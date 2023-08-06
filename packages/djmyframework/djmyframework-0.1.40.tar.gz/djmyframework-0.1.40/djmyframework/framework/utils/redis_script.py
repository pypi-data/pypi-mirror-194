"""Redis Lua Script"""
import redis
from django.core.cache import cache

# 通用 额度校验 存在键&原值大于入参则减去并返回 否则返回空
common_limit = """
redis.replicate_commands();
local cache_number = tonumber(redis.call("get", KEYS[1]))
if(type(cache_number)~="number") then cache_number = 0 end
local sub_val = cache_number - tonumber(ARGV[1])
if sub_val >= 0 then
redis.call("set", KEYS[1], sub_val)
return sub_val
end
"""

# 取餐柜分配格子
# 记录一个坑: redis lua 使用 function 设计的不好容易导致失去原子性
cupboard_ceil_dealing_script = """
redis.replicate_commands();
-- 初始化参数
local big_ceil_len = redis.call("scard", KEYS[1])
local little_ceil_len = redis.call("scard", KEYS[2])
local foods_json = cjson.decode(ARGV[1])
local big_ceil_size = tonumber(ARGV[2])
local little_ceil_size = tonumber(ARGV[3])
local big_ceil_num = 0
local little_ceil_num = 0
local big_ceil_list = {}
local little_ceil_list = {}
local total_counts = 0
local _ceil_num = 0
-- 获取总份数
for obj_id, foods_count in pairs(foods_json) do
    total_counts = total_counts + foods_count
end
-- 检查格子是否足够 总份数
if total_counts > big_ceil_len * big_ceil_size + little_ceil_len * little_ceil_size then
    return nil
elseif total_counts <= 0 then
    return nil
end
for obj_id, foods_count in pairs(foods_json) do
    -- 重置变量
    big_ceil_num = 0
    little_ceil_num = 0
    -- 检查格子是否足够 子订单份数
    if foods_count > big_ceil_len * big_ceil_size + little_ceil_len * little_ceil_size then
        -- 由于按照子单分配 所以可能会出现冗余 导致不够分配 这种情况要进行回退
        for k,v in pairs(big_ceil_list) do
            redis.call("sadd", KEYS[1], v)
        end
        for k,v in pairs(little_ceil_list) do
            redis.call("sadd", KEYS[2], v)
        end
        return nil
    end
    -- 计算最优分配方式
    while (foods_count > big_ceil_size and big_ceil_num < big_ceil_len)
    do
        foods_count = foods_count - big_ceil_size
        big_ceil_num = big_ceil_num + 1
    end
    while (foods_count > 0)
    do
        foods_count = foods_count - little_ceil_size
        little_ceil_num = little_ceil_num + 1
    end
    -- 分配格子
    foods_json[obj_id] = {}
    foods_json[obj_id]["big_ceil_arr"] = {}
    foods_json[obj_id]["little_ceil_arr"] = {}
    for i=1, big_ceil_num do
        _ceil_num = redis.call("spop", KEYS[1])
        table.insert(big_ceil_list, _ceil_num)
        foods_json[obj_id]["big_ceil_arr"][i] = _ceil_num
    end
    for i=1, little_ceil_num do
        _ceil_num = redis.call("spop", KEYS[2])
        table.insert(little_ceil_list, _ceil_num)
        foods_json[obj_id]["little_ceil_arr"][i] = _ceil_num
    end
    big_ceil_len = big_ceil_len - big_ceil_num
    little_ceil_len = little_ceil_len - little_ceil_num
end
redis.call("set", KEYS[3], big_ceil_len * big_ceil_size + little_ceil_len * little_ceil_size)
return cjson.encode(foods_json)
"""

sub_number_script = """
redis.replicate_commands();
local cache_number = redis.call("get", KEYS[1]) or 0
local sub_number = tonumber(ARGV[1] or 0)
local result = cache_number - sub_number
if result < 0 then
    return 0
end
redis.call("set", KEYS[1], result)
return 1
"""

bulk_push_script = """
redis.replicate_commands();
for k,v in pairs(ARGV) do
    redis.call(KEYS[1], KEYS[2], v)
end
"""

# push_distinct_val_to_list

redis_client: redis.Redis = cache.client.get_client()
common_limit = redis_client.register_script(common_limit)
sub_ceil = redis_client.register_script(cupboard_ceil_dealing_script)
# sub_ceil(keys=[f"{CACHE_CUPBOARD_BIG_CEIL_LIST}_{cupboard_id}",
#                f"{CACHE_CUPBOARD_LITTLE_CEIL_LIST}_{cupboard_id}",
#                f"{CACHE_CUPBOARD_EMPTY_CEIL_COUNT}_{cupboard_id}"],
#          args=[json.dumps(reservation_item, ensure_ascii=False),
#                big_ceil_size, little_ceil_size])
# -> b'{"1":{"little_ceil_arr":["5","6"],"big_ceil_arr":["1","2","3","4"]},
#       "2":{"little_ceil_arr":["7","8"],"big_ceil_arr":{}}}'
sub_number = redis_client.register_script(sub_number_script)
bulk_push = redis_client.register_script(bulk_push_script)

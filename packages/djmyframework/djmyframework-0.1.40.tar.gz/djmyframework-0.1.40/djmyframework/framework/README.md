## 基础框架

### 特性

- 自动路由
- api文档生成
- 模板生成 app
    - python manage.py create_app app_name
- crud_api 命令快速生成代码 controller 方式
    - python manage.py create_curd_api myadmin.Admin -f
- 请求参数 返回参数 格式定义

### 使用方法

1. 创建 app

```angular2html
python manage.py create_app test_framework_app
```

> 修改 apps.py 的 verbose_name

2. settings INSTALLED_APPS 添加新的 app
3. 定义 Model,创建 curd 样板

```
python manage.py create_curd_api test_framework_app.FooModel -f
```

4. 访问 http://0.0.0.0:8000/__redoc 查看自动生产的 API 文档
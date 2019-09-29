# 教室信息Demo

### 知晓云数据库

- 创建

  直接在知晓云面板上新建的数据库teachers，手动添加的行和列

  ![1](picture\1.JPG)

- 连接

  没有用Django的数据库，所以就把获取token的函数写在了新建的app（TestModel）的models.py里面（虽然我也不知道要不要）

  用知晓云提供的client_id和client_secret，还有生成的table_id获取token

  ```python
  class Connect():
      code_config = {
          'url': 'https://cloud.minapp.com/api/oauth2/hydrogen/openapi/authorize/',
          'headers': {'Content-Type': 'application/json'}
      }
      code_data = {
          'client_id': '0e5d4e5846999c4b7cab',
          'client_secret': '397e56a9656b96f177c248d8804290d9aefcb35b'
      }
      token_config = {
          'url': 'https://cloud.minapp.com/api/oauth2/access_token/',
          'headers': {'Content-Type': 'application/json'}    
      }
      token_data = {
          'client_id': '0e5d4e5846999c4b7cab',
          'client_secret': '397e56a9656b96f177c248d8804290d9aefcb35b',
          'grant_type': 'authorization_code',
          'code': None
      }
      table_id = '78695'
  
      code_response = requests.post(url=code_config['url'], 
              data=json.dumps(code_data), 
              headers=code_config['headers'])
      token_data['code'] = code_response.json().get('code')
      token_response = requests.post(url=token_config['url'], 
              data=json.dumps(token_data), 
              headers=token_config['headers'])
      token = token_response.json().get('access_token')
  ```

  

### 功能

操作页面：`http://127.0.0.1:8080/view`

view.html放在templates里面

#### 删除某个教师

- 接口函数：deleteTeacher()

- 输入：教师姓名(name)

- `record_name  =  request.GET['name']`

- get_id()：用record_name在表中查询找到该教师在表中的id

  - 接口：`GET https://cloud.minapp.com/oserve/v1/table/:table_id/record/`

  - 参数：

    ```python
    where_ = {
                'name': {'$eq': record_name},
            }
    ```

  - response

    ```json
    {
        "meta": {
            "limit": 1,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 1
        },
        "objects": [
            {
                "_id": "5d2725d456bb140c6e65315c",
                "college": "东大",
                "created_at": 1562846676,
                "created_by": 77836045,
                "id": "5d2725d456bb140c6e65315c",
                "name": "十",
                "read_perm": [
                    "user:anonymous"
                ],
                "title": "教授",
                "updated_at": 1562846676,
                "write_perm": [
                    "user:anonymous"
                ]
            }
        ]
    }
    ```

- deleteTeacher()
  - 接口：`DELETE https://cloud.minapp.com/oserve/v1/table/:table_id/record/:record_id/`
  - 返回查询得到的name,college,titile

#### 返回某个学院某个职称的所有老师及学院评价

- 接口函数：getSomeTeacher

- 输入：学院（college），职称（title）

- `record_college = request.GET['college']
  record_title = request.GET['title']`

- 用college和title查询所有老师信息

  - 接口：`GET https://cloud.minapp.com/oserve/v1/table/:table_id/record/`

  - 参数

    ```python
    where_ = {
                'college': {'$eq': record_college},
                'title': {'$eq': record_title},
            }
    ```

- 用len()返回列表长度（即教师数量）比较后返回evaluation
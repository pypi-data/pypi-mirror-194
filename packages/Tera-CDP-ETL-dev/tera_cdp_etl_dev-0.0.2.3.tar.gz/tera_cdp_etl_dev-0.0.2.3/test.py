# from tera_etl import quality_control as qc
# schema = {
#     "UserId" : "int",
#     "HomePhone" : "string",
#     "WorkPhone" : ["string", "null"],
#     "Address" : {
#         "HouseNo": "string",
#         "Streetname": "string",
#         "Ward": "string",
#         "District": "string",
#         "Province": "string",
#         "Country": "string"
#     },
#     "Firstname" : "string",
#     "Lastname" : "string",
#     "Gender" : "string",
#     "RegisterDate" : "datetime",
#     "Status" : "string",
#     "DataSource" : "string",
#     "Source" : "string",
#     "EventId" : "string"
# }
# data = {
#     "UserId": 202201439424,
#     "HomePhone": "0912919543",
#     "WorkPhone": None,""
#     "Address": {
#         "HouseNo": "",
#         "Streetname": "",
#         "Ward": "ẤP HÒA CƯỜNG, Xã Minh Hoà",
#         "District": "Huyện Dầu Tiếng",
#         "Province": "Tỉnh Bình Dương",
#         "Country": "Việt Nam"
#     },
#     "Firstname": "TRẦN VĂN ",
#     "Lastname": "TÙNG",
#     "Gender": "Male",
#     "RegisterDate": "2022-01-01T00:00:00.00Z",
#     "Status": "True",
#     "DataSource": "VTVHyundai",
#     "Source": "VTVHyundai",
#     "EventId": "VTVHyundai_IngestProfile_202201439424"
# }


# from tera_etl import quality_control as qc
# structures = {
#     "Fields": [
#       {"Name": "UserId", "FieldType": "string", "Validation": "String,MustHave", "Comment": "id của user trong hệ thống, phải là kiểu string" },
#       {"Name": "HomePhone", "FieldType": ["string", "null"], "Comment": "Nếu không có thì để trống" },
#       {"Name": "WorkPhone", "FieldType": ["string", "null"], "Comment": "Nếu không có thì để trống" },
#       {"Name": "AddrHouseNo", "FieldType": "string", "Comment": "Số nhà" },
#       {"Name": "AddrStreetName", "FieldType": "string", "Comment": "Tên đường" },
#       {"Name": "AddrWard", "FieldType": "string", "Comment": "Phường / Xã" },
#       {"Name": "AddrDistrict", "FieldType": "string", "Comment": "Quận / Huyện / Thành Phố trực thuộc tỉnh" },
#       {"Name": "AddrProvince", "FieldType": "string", "Comment": "Tỉnh / Thành phố trực thuộc TW" },
#       {"Name": "AddrCountry", "FieldType": "string", "Validation": "Iso Country Code", "Comment": "Tên nước - ISO Country Code - E.g. VN" },
#       {"Name": "Firstname", "FieldType": "string", "Comment": "Tên" },
#       {"Name": "Lastname", "FieldType": "string", "Comment": "Họ và chữ lót" },
#       {"Name": "Gender", "FieldType": "string", "Comment": "Giới tính, tiếng anh, để khỏi bị nhầm lẫn", "Validation": "Male/Female/Other" },
#       {"Name": "RegisterDate", "FieldType": "datetime", "Comment": "Ngày đăng ký vào hệ thống" },
#       {"Name": "DataSource", "FieldType": "string", "Comment": "DataProviderName" },
#       {"Name": "MaritalStatus", "FieldType": "string", "Comment": "Tình trạng hôn nhân", "Validation": "Single/Married" }
#     ]
#   }
# data = {
#     "UserId": "202201439260",
#     "HomePhone": "0369841490",
#     "WorkPhone": None,
#     "AddrHouseNo": "",
#     "AddrStreetName": "",
#     "AddrWard": "15 NGÕ 341, Phường Xuân Phương",
#     "AddrDistrict": "Quận Nam Từ Liêm",
#     "AddrProvince": "Thành phố Hà Nội",
#     "AddrCountry": "Việt Nam",
#     "Firstname": "NGUYỄN THỊ BÍCH ",
#     "Lastname": "HIỀN",
#     "Gender": "Female",
#     "RegisterDate": "2022-01-01T00:00:00.00Z",
#     "DataSource": "VTVHyundai",
#     "MaritalStatus": "Single"
# }
# schema = {
#     'UserId': 'string',
#     'HomePhone': ['string', 'null'],
#     'WorkPhone': ['string', 'null'],
#     'AddrHouseNo': 'string',
#     "AddrStreetName": "string",
#     'AddrWard': 'string',
#     'AddrDistrict': 'string',
#     'AddrProvince': 'string',
#     'AddrCountry': 'string',
#     'Firstname': 'string',
#     'Lastname': 'string',
#     'Gender': 'string',
#     'RegisterDate': 'datetime',
#     'DataSource': 'string',
#     'MaritalStatus': 'string'
# }

# schema_dict={}
# for field in structures["Fields"]:
#     schema_dict[field["Name"]] = field["FieldType"]
# print(schema_dict)
# qc_type = qc.classify_data(data_chunk=data, schema=schema)
# print(qc_type)
# print("AddrStreetName" not in schema.keys())
# for field in data:
#     if field not in list(schema.keys()):
#         print(list(schema.keys()))
#         print(field)

# import json
# f = open("data.json")
# datas = json.load(f)
# f.close()
# for data in datas:
#     # print(data)
#     qc_result = qc.classify_data(data_chunk=data, schema=schema)
#     if qc_result["qc_type"] == qc.QualityControlResult.ACCEPTED:
#         # print(qc_result["qc_type"])
#         pass
#     else:
#         print(qc_result["errors"])

# schema = {
#     'UserId': 'string',
#     'HomePhone': ['string', 'null'],
#     'WorkPhone': ['string', 'null'],
#     'AddrHouseNo': 'string',
#     "AddrStreetName": "string",
#     'AddrWard': 'string',
#     'AddrDistrict': 'string',
#     'AddrProvince': 'string',
#     'AddrCountry': 'string',
#     'Firstname': 'string',
#     'Lastname': 'string',
#     'Gender': 'string',
#     'RegisterDate': 'datetime',
#     'DataSource': 'string',
#     'MaritalStatus': 'string'
# }

# from marshmallow import Schema, fields, validate
# from marshmallow.validate import Regexp, Length, OneOf

from tera_etl import quality_control as qc

data = {
    "UserId": "202201439260",
    "HomePhone": "0369841490",
    "WorkPhone": None,
    "AddrHouseNo": "",
    "AddrStreetName": "",
    "AddrWard": "15 NGÕ 341, Phường Xuân Phương",
    "AddrDistrict": "Quận Nam Từ Liêm",
    "AddrProvince": "Thành phố Hà Nội",
    "AddrCountry": "Việt Nam",
    "Firstname": "NGUYỄN THỊ BÍCH ",
    "Lastname": "HIỀN",
    "Gender": "Female",
    "RegisterDate": "2022-01-01T00:00:00.00Z",
    "DataSource": "VTVHyundai",
    "MaritalStatus": "Single"
}

# class UserProfileSchema(Schema):
#     UserId = fields.String(required=True)
#     HomePhone = fields.String(allow_none=True)
#     WorkPhone = fields.String(allow_none=True)
#     AddrHouseNo = fields.String()
#     AddrStreetName = fields.String()
#     AddrWard = fields.String()
#     AddrDistrict = fields.String()
#     AddrProvince = fields.String()
#     AddrCountry = fields.String()
#     Firstname = fields.String()
#     Lastname = fields.String()
#     Gender = fields.String(
#         validate=[
#             validate.OneOf(["Male", "Female", "Other"])
#         ]
#     )
#     RegisterDate = fields.String()
#     DataSource = fields.String()
#     MaritalStatus = fields.String(
#         validate=[
#             validate.OneOf(["Single", "Married"])
#         ]
#     )


import json
f = open("data.json")
datas = json.load(f)
f.close()
# userProfileSchema = UserProfileSchema(many=True)
for data in datas:
    a = qc.classify_data(data_chunk=data,schema_name="UserProfileSchema")
    if a["qc_type"] != qc.QualityControlResult.ACCEPTED:
        print(a)

#     errors = userProfileSchema.validate(data)
#     if errors:
#         print(data)
# print(errors.keys())

    # UserId = fields.Str(required=True)
    # HomePhone = fields.Str(required=False)
    # WorkPhone = fields.Str(required=False)
    # AddrHouseNo = fields.Str(required=True)
    # AddrStreetName = fields.Str(required=True)
    # AddrWard = fields.Str(required=True)
    # AddrDistrict = fields.Str(required=True)
    # AddrProvince = fields.Str(required=True)
    # AddrCountry = fields.Str(required=True)
    # Firstname = fields.Str(required=True)
    # Lastname = fields.Str(required=True)
    # Gender = fields.Str(
    #     required=True,
    #     validate=[
    #         OneOf(choices=["Male","Female", "Other"])
    #     ]
    # )
    # RegisterDate = fields.Str(required=True)
    # DataSource = fields.Str(required=True)
    # MaritalStatus = fields.Str(
    #     required=True,
    #     validate=[
    #         OneOf(choices=["Single", "Married"])
    #     ]
    # )
# print(globals())
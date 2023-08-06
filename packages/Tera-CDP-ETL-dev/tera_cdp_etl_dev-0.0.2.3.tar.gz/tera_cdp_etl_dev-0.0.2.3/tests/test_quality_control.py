import tera_etl.quality_control as qc

def test_perform_quality_control():
    schema_name = "UserProfileSchema"
    data = {
        "UserId": "090349324324",
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
    qc_result = qc.classify_data(data_chunk=data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.ACCEPTED

    new_case_data = data.copy()
    new_case_data["UserId"] = None
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'UserId': ['Field may not be null.']}

    new_case_data = data.copy()
    new_case_data["Gender"] = "TEST"
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'Gender': ['Must be one of: Male, Female, Other.']}

    new_case_data = data.copy()
    new_case_data["MaritalStatus"] = "TEST"
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'MaritalStatus': ['Must be one of: Single, Married.']}

    new_case_data = data.copy()
    del new_case_data['UserId']
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'UserId': ['Missing data for required field.']}


    new_case_data = data.copy()
    new_case_data['Firstname'] = None
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'Firstname': ['Field may not be null.']}


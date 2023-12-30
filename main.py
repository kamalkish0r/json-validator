class JsonValidator:
    """
    Class to validate a JSON against a schema
    """
    
    def validate_schema(self, json_data: dict, schema: dict) -> bool:
        """
        Validate JSON data against a schema
        
        Args:
            json_data: The JSON data to validate 
            schema: The schema to validate against
            
        Returns:
            True if validation succeeds, False otherwise
        """
        
        # Check required fields
        required = schema.get("required", [])
        for field in required:
            if field not in json_data:
                print(f"Required field {field} missing")
                return False
        
        # Check one of many fields present
        one_of = schema.get("oneOf", [])
        one_of_present = False
        for field in one_of:
            if field in json_data:
                one_of_present = True
                break
        if not one_of_present:
            print(f"None of the oneOf fields {one_of} are present")
            return False
        
        # Check either or
        either_or = schema.get("eitherOr", [])
        if len(either_or) == 2:
            field1, field2 = either_or
            if field1 in json_data and field2 in json_data:
                print(f"Either or fields {field1} and {field2} both present")
                return False
            
        # Check mutually exclusive
        mutually_exclusive = schema.get("mutuallyExclusive", [])
        if len(mutually_exclusive) == 2:
            field1, field2 = mutually_exclusive
            if field1 in json_data and field2 in json_data:
                print(f"Mutually exclusive fields {field1} and {field2} both present")
                return False
            
        # Check enum values
        enums = schema.get("enum", {})
        for field, values in enums.items():
            if field in json_data:
                if json_data[field] not in values:
                    print(f"Field {field} has invalid value, must be one of {values}")
                    return False
            
        return True


if __name__ == '__main__':
    schema = {
        "required": ["id", "name"],
        "oneOf": ["home_phone", "cell_phone", "work_phone"],
        "eitherOr": ["birth_date", "govt_id"],
        "mutuallyExclusive": ["field1", "field2"],
        "enum": {"day": ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]}
    }

    data = {
        "id": "123",
        "name": "John Doe",
        "home_phone": "555-1234",
        "day": "MO"
    }

    validator = JsonValidator()
    isValid = validator.validate_schema(data, schema)
    print(isValid) 
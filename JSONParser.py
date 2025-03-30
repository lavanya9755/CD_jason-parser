class JSONParser:
    def __init__(self, json_string):
        self.json_string = json_string.strip()
        self.index = 0  # Pointer to track parsing

    def parse(self):
        value = self._parse_value()
        self._skip_whitespace()
        if self.index != len(self.json_string):  
            raise ValueError("Unexpected characters at end of JSON")
        return value

    def _parse_value(self):
        self._skip_whitespace()
        if self.json_string[self.index] == '"':  
            return self._parse_string()
        elif self.json_string[self.index].isdigit() or self.json_string[self.index] == '-':  
            return self._parse_number()
        elif self.json_string[self.index] == '{':  
            return self._parse_object()
        elif self.json_string[self.index] == '[':  
            return self._parse_array()
        elif self.json_string.startswith("true", self.index):
            self.index += 4
            return True
        elif self.json_string.startswith("false", self.index):
            self.index += 5
            return False
        elif self.json_string.startswith("null", self.index):
            self.index += 4
            return None
        else:
            raise ValueError(f"Invalid JSON value at index {self.index}")

    def _parse_string(self):
        self.index += 1  # Skip opening "
        start = self.index
        while self.json_string[self.index] != '"':
            self.index += 1
        result = self.json_string[start:self.index]
        self.index += 1  # Skip closing "
        return result

    def _parse_number(self):
        start = self.index
        while self.index < len(self.json_string) and (self.json_string[self.index].isdigit() or self.json_string[self.index] in ".-"):
            self.index += 1
        return float(self.json_string[start:self.index]) if "." in self.json_string[start:self.index] else int(self.json_string[start:self.index])

    def _parse_object(self):
        obj = {}
        self.index += 1  # Skip {
        while self.json_string[self.index] != '}':
            self._skip_whitespace()
            key = self._parse_string()
            self._skip_whitespace()
            if self.json_string[self.index] != ':':
                raise ValueError("Expected ':' after key in object")
            self.index += 1  # Skip :
            obj[key] = self._parse_value()
            self._skip_whitespace()
            if self.json_string[self.index] == '}':
                break
            if self.json_string[self.index] != ',':
                raise ValueError("Expected ',' in object")
            self.index += 1  # Skip ,
        self.index += 1  # Skip }
        return obj

    def _parse_array(self):
        arr = []
        self.index += 1  # Skip [
        while self.json_string[self.index] != ']':
            self._skip_whitespace()
            arr.append(self._parse_value())
            self._skip_whitespace()
            if self.json_string[self.index] == ']':
                break
            if self.json_string[self.index] != ',':
                raise ValueError("Expected ',' in array")
            self.index += 1  # Skip ,
        self.index += 1  # Skip ]
        return arr

    def _skip_whitespace(self):
        while self.index < len(self.json_string) and self.json_string[self.index] in " \n\t\r":
            self.index += 1

# Testing the parser
json_text = '{"name": "John", "age": 30, "isStudent": false, "marks": [90, 85, 88]}'
parser = JSONParser(json_text)
parsed_data = parser.parse()
print(parsed_data)  # Expected Output: {'name': 'John', 'age': 30, 'isStudent': False, 'marks': [90, 85, 88]}

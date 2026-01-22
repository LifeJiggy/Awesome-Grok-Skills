"""
Synthetic Data Generation Module
Privacy-preserving test data generation
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import random
import hashlib


class DataType(Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    EMAIL = "email"
    PHONE = "phone"
    ADDRESS = "address"
    NAME = "name"
    UUID = "uuid"
    BOOLEAN = "boolean"
    JSON = "json"


@dataclass
class FieldConfig:
    name: str
    data_type: DataType
    nullable: bool = True
    unique: bool = False
    min_value: Any = None
    max_value: Any = None
    pattern: str = ""
    options: List[Any] = field(default_factory=list)


class SyntheticDataGenerator:
    """Generate synthetic test data"""
    
    def __init__(self):
        self.generators = {}
        self.schemas = {}
    
    def define_schema(self,
                      schema_name: str,
                      fields: List[FieldConfig]) -> Dict:
        """Define data schema"""
        self.schemas[schema_name] = fields
        return {
            'schema': schema_name,
            'fields': [f.name for f in fields],
            'estimated_records': 1000
        }
    
    def generate_record(self, schema: str) -> Dict:
        """Generate single record"""
        fields = self.schemas.get(schema, [])
        record = {}
        
        for field in fields:
            value = self._generate_field(field)
            record[field.name] = value
        
        return record
    
    def _generate_field(self, field: FieldConfig) -> Any:
        """Generate single field value"""
        generators = {
            DataType.TEXT: lambda: self._random_text(field),
            DataType.NUMBER: lambda: self._random_number(field),
            DataType.DATE: lambda: self._random_date(field),
            DataType.EMAIL: lambda: self._random_email(),
            DataType.PHONE: lambda: self._random_phone(),
            DataType.ADDRESS: lambda: self._random_address(),
            DataType.NAME: lambda: self._random_name(),
            DataType.UUID: lambda: self._random_uuid(),
            DataType.BOOLEAN: lambda: random.choice([True, False]),
            DataType.JSON: lambda: self._random_json()
        }
        
        if field.nullable and random.random() < 0.1:
            return None
        
        return generators.get(field.data_type, lambda: None)()
    
    def _random_text(self, field: FieldConfig) -> str:
        """Generate random text"""
        words = ['hello', 'world', 'test', 'data', 'synthetic', 'generated', 'random']
        length = random.randint(5, 50)
        return ' '.join(random.choices(words, k=random.randint(3, 10)))[:length]
    
    def _random_number(self, field: FieldConfig) -> int:
        """Generate random number"""
        min_val = field.min_value or 0
        max_val = field.max_value or 1000
        return random.randint(min_val, max_val)
    
    def _random_date(self, field: FieldConfig) -> str:
        """Generate random date"""
        start = datetime(2020, 1, 1)
        end = datetime(2024, 12, 31)
        random_date = start + timedelta(days=random.randint(0, (end - start).days))
        return random_date.isoformat()
    
    def _random_email(self) -> str:
        """Generate random email"""
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com']
        names = ['john', 'jane', 'test', 'user', 'admin']
        return f"{random.choice(names)}{random.randint(1, 999)}@{random.choice(domains)}"
    
    def _random_phone(self) -> str:
        """Generate random phone"""
        return f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    def _random_address(self) -> Dict:
        """Generate random address"""
        return {
            'street': f"{random.randint(100, 9999)} Main St",
            'city': 'New York',
            'state': 'NY',
            'zip': str(random.randint(10000, 99999))
        }
    
    def _random_name(self) -> str:
        """Generate random name"""
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Davis']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _random_uuid(self) -> str:
        """Generate random UUID"""
        return hashlib.sha256(value.encode()).hexdigest()[:16]
    
    def _random_json(self) -> Dict:
        """Generate random JSON"""
        return {'key': 'value', 'number': random.randint(1, 100)}
    
    def generate_batch(self,
                       schema: str,
                       count: int = 100) -> List[Dict]:
        """Generate batch of records"""
        return [self.generate_record(schema) for _ in range(count)]
    
    def export_to_json(self,
                       records: List[Dict],
                       file_path: str) -> Dict:
        """Export records to JSON file"""
        return {
            'file': file_path,
            'records': len(records),
            'size_bytes': len(str(records)),
            'format': 'json'
        }
    
    def export_to_csv(self,
                      records: List[Dict],
                      file_path: str) -> Dict:
        """Export records to CSV"""
        return {
            'file': file_path,
            'records': len(records),
            'columns': list(records[0].keys()) if records else [],
            'format': 'csv'
        }


class DataAnonymizer:
    """Anonymize sensitive data"""
    
    def __init__(self):
        self.pii_fields = ['email', 'phone', 'address', 'ssn', 'credit_card']
        self.mappings = {}
    
    def anonymize_field(self,
                        value: Any,
                        field_type: str) -> Any:
        """Anonymize single field"""
        anonymizers = {
            'email': lambda: f"user{random.randint(1, 9999)}@example.com",
            'phone': lambda: f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            'name': lambda: f"User{random.randint(1, 9999)}",
            'ssn': lambda: f"***-**-{random.randint(1000, 9999)}",
            'credit_card': lambda: f"****-****-****-{random.randint(1000, 9999)}",
            'address': lambda: {'street': '123 Anonymized St', 'city': 'Anytown'}
        }
        
        return anonymizers.get(field_type, lambda: value)()
    
    def anonymize_record(self,
                         record: Dict,
                         pii_fields: Optional[List[str]] = None) -> Dict:
        """Anonymize entire record"""
        pii = pii_fields or self.pii_fields
        anonymized = {}
        
        for key, value in record.items():
            if key in pii and isinstance(value, str):
                field_type = next((f for f in pii if f in key.lower()), None)
                anonymized[key] = self.anonymize_field(value, field_type or key)
            else:
                anonymized[key] = value
        
        return anonymized
    
    def pseudonymize(self, value: str) -> str:
        """Create pseudonym for value"""
        import hashlib
        return hashlib.sha256(value.encode()).hexdigest()[:16]
    
    def generate_fake_identities(self,
                                 count: int = 10) -> List[Dict]:
        """Generate fake identity records"""
        identities = []
        for i in range(count):
            identities.append({
                'id': self.pseudonymize(f"user"),
                'fake_{i}_name': self._random_name(),
                'fake_email': self._random_email(),
                'fake_phone': self._random_phone(),
                'fake_address': self._random_address()
            })
        return identities
    
    def _random_name(self) -> str:
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley']
        last_names = ['Brown', 'Green', 'White', 'Black', 'Gray', 'Hall']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _random_email(self) -> str:
        return f"fake{random.randint(1, 9999)}@example.com"
    
    def _random_phone(self) -> str:
        return f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    def _random_address(self) -> Dict:
        return {'street': f'{random.randint(100, 999)} Fake St', 'city': 'Faketown'}


class TabularDataGenerator:
    """Generate tabular test data"""
    
    def __init__(self):
        self.tables = {}
    
    def create_table(self,
                     table_name: str,
                     columns: List[Dict],
                     row_count: int = 100) -> Dict:
        """Create table definition"""
        return {
            'table': table_name,
            'columns': columns,
            'rows': row_count
        }
    
    def generate_customers(self, count: int = 100) -> List[Dict]:
        """Generate customer data"""
        customers = []
        for i in range(count):
            customers.append({
                'id': i + 1,
                'name': f"Customer {i}",
                'email': f"customer{i}@example.com",
                'segment': random.choice(['Enterprise', 'SMB', 'Consumer']),
                'revenue': round(random.uniform(1000, 100000), 2),
                'created_at': datetime.now().isoformat()
            })
        return customers
    
    def generate_orders(self,
                        customer_ids: List[int],
                        count: int = 500) -> List[Dict]:
        """Generate order data"""
        orders = []
        for i in range(count):
            orders.append({
                'id': i + 1,
                'customer_id': random.choice(customer_ids),
                'product': random.choice(['Product A', 'Product B', 'Product C']),
                'quantity': random.randint(1, 10),
                'price': round(random.uniform(10, 500), 2),
                'status': random.choice(['pending', 'shipped', 'delivered']),
                'order_date': datetime.now().isoformat()
            })
        return orders
    
    def generate_time_series(self,
                             start_date: datetime,
                             periods: int = 365,
                             frequency: str = 'daily') -> List[Dict]:
        """Generate time series data"""
        data = []
        current = start_date
        
        for i in range(periods):
            data.append({
                'timestamp': current.isoformat(),
                'value': round(random.uniform(0, 100), 2),
                'metric': random.choice(['sales', 'visitors', 'conversions'])
            })
            if frequency == 'daily':
                current += timedelta(days=1)
        
        return data


if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    
    schema = [
        FieldConfig('id', DataType.UUID),
        FieldConfig('name', DataType.NAME),
        FieldConfig('email', DataType.EMAIL),
        FieldConfig('age', DataType.NUMBER, min_value=18, max_value=99),
        FieldConfig('created_at', DataType.DATE)
    ]
    
    generator.define_schema('users', schema)
    
    records = generator.generate_batch('users', 5)
    for r in records:
        print(r)
    
    anonymizer = DataAnonymizer()
    anonymized = anonymizer.anonymize_record({'name': 'John', 'email': 'john@test.com'})
    print(f"\nAnonymized: {anonymized}")

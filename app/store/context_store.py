from typing import Dict, Any, Optional


class ContextStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContextStore, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the context store with empty values"""
        self.context: Dict[str, Any] = {
            'user_details': {
                'name': None,
                'location': None,
                'address': None,
                'phone': None,
                'email': None
            },
            'connection_details': {
                'connection_type': None,
                'provider_id': None,
                'item_id': None,
                'selection_id': None,
                'transaction_id': None,
                'fulfillment_id': None,
                'customer_name': None,
                'customer_phone': None,
                'customer_email': None,
                'order_id': None
            },
            'solar_details': {
                'provider_id': None,
                'item_id': None,
                'selection_id': None,
                'transaction_id': None,
                'fulfillment_id': None,
                'customer_name': None,
                'customer_phone': None,
                'customer_email': None,
                'order_id': None,
                'system_size': None,
                'installation_type': None
            },
            'service_details': {
                'provider_id': None,
                'item_id': None,
                'selection_id': None,
                'transaction_id': None,
                'fulfillment_id': None,
                'customer_name': None,
                'customer_phone': None,
                'customer_email': None,
                'order_id': None,
                'installation_date': None,
                'installation_address': None
            },
            'subsidy_details': {
                'provider_id': None,
                'item_id': None,
                'selection_id': None,
                'transaction_id': None,
                'fulfillment_id': None,
                'customer_name': None,
                'customer_phone': None,
                'customer_email': None,
                'order_id': None,
                'subsidy_type': None,
                'subsidy_amount': None
            },
            'transaction_history': {}
        }

    def update_user_details(self, **kwargs) -> None:
        """Update user details in the context"""
        self.context['user_details'].update(kwargs)

    def update_connection_details(self, **kwargs) -> None:
        """Update connection details in the context"""
        self.context['connection_details'].update(kwargs)

    def update_solar_details(self, **kwargs) -> None:
        """Update solar details in the context"""
        self.context['solar_details'].update(kwargs)

    def update_service_details(self, **kwargs) -> None:
        """Update service details in the context"""
        self.context['service_details'].update(kwargs)

    def update_subsidy_details(self, **kwargs) -> None:
        """Update subsidy details in the context"""
        self.context['subsidy_details'].update(kwargs)

    def add_transaction_history(self, action: str, data: Dict) -> None:
        """Add transaction data to history"""
        self.context['transaction_history'][action] = data

    def get_user_details(self) -> Dict:
        """Get all user details"""
        return self.context['user_details']

    def get_connection_details(self) -> Dict:
        """Get all connection details"""
        return self.context['connection_details']

    def get_solar_details(self) -> Dict:
        """Get all solar details"""
        return self.context['solar_details']

    def get_service_details(self) -> Dict:
        """Get all service details"""
        return self.context['service_details']

    def get_subsidy_details(self) -> Dict:
        """Get all subsidy details"""
        return self.context['subsidy_details']

    def get_transaction_history(self) -> Dict:
        """Get complete transaction history"""
        return self.context['transaction_history']

    def get_order_id(self, agent_type: str) -> Optional[str]:
        """Get order ID for a specific agent type"""
        details_map = {
            'connection': 'connection_details',
            'solar': 'solar_details',
            'service': 'service_details',
            'subsidy': 'subsidy_details'
        }
        if agent_type not in details_map:
            raise ValueError(f"Invalid agent type: {agent_type}")
        return self.context[details_map[agent_type]].get('order_id')

    def copy_user_details_to_agent(self, agent_type: str) -> None:
        """Copy user details to a specific agent's details"""
        details_map = {
            'connection': 'connection_details',
            'solar': 'solar_details',
            'service': 'service_details',
            'subsidy': 'subsidy_details'
        }
        if agent_type not in details_map:
            raise ValueError(f"Invalid agent type: {agent_type}")
        
        user_details = self.get_user_details()
        self.context[details_map[agent_type]].update({
            'customer_name': user_details.get('name'),
            'customer_phone': user_details.get('phone'),
            'customer_email': user_details.get('email')
        })

    def get_value(self, key: str, subkey: Optional[str] = None) -> Any:
        """Get a specific value from the context"""
        if subkey:
            return self.context.get(key, {}).get(subkey)
        return self.context.get(key)

    def reset(self) -> None:
        """Reset the context store to initial state"""
        self._initialize()
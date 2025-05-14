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
                'transaction_id': None
            },
            'transaction_history': {}
        }

    def update_user_details(self, **kwargs) -> None:
        """Update user details in the context"""
        self.context['user_details'].update(kwargs)

    def update_connection_details(self, **kwargs) -> None:
        """Update connection details in the context"""
        self.context['connection_details'].update(kwargs)

    def add_transaction_history(self, action: str, data: Dict) -> None:
        """Add transaction data to history"""
        self.context['transaction_history'][action] = data

    def get_user_details(self) -> Dict:
        """Get all user details"""
        return self.context['user_details']

    def get_connection_details(self) -> Dict:
        """Get all connection details"""
        return self.context['connection_details']

    def get_transaction_history(self) -> Dict:
        """Get complete transaction history"""
        return self.context['transaction_history']

    def get_value(self, key: str, subkey: Optional[str] = None) -> Any:
        """Get a specific value from the context"""
        if subkey:
            return self.context.get(key, {}).get(subkey)
        return self.context.get(key)

    def reset(self) -> None:
        """Reset the context store to initial state"""
        self._initialize()
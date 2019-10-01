"""
A Mapping module
"""

class DataMapping:
    """DataMapping"""
    def __init__(self, data: dict, keys_map: dict):

        """__init__

        :param data:
        :type data: dict
        :param keys_map:
        :type keys_map: dict

        data = {'username': 'John', 'email': 'john@example.com'}
        keys_map = {'username': 'user', 'email': 'myemail'}

        """

        self.data = data
        self.keys_map = keys_map

    async def mapping(self) -> dict:
        """mapping

        :rtype: dict
        """
        return {val: self.data[key]
                for key, val in self.keys_map.items() if key in self.data}

import unittest
import os
import yaml
from bot.conf import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        # 创建测试配置文件
        self.test_config_file = "test_config.yml"
        test_config = {
            "wechat": {
                "alias": [
                    {
                        "wxid": "wxid_1",
                        "alias": ["爸爸", "康强"]
                    },
                    {
                        "wxid": "wxid_2",
                        "alias": ["妈妈", "园园"]
                    }
                ],
                "contacts": [
                    {
                        "wxid": "wxid_1",
                        "alias": ["爸爸", "康强"]
                    },
                    {
                        "wxid": "wxid_2",
                        "alias": ["妈妈", "园园"]
                    },
                    {
                        "wxid": "wxid_3",
                        "alias": ["小明", "明明"]
                    }
                ]
            },
            "test": {
                "string": "value",
                "number": 123,
                "boolean": True,
                "nested": {
                    "key": "nested_value"
                }
            }
        }
        
        with open(self.test_config_file, 'w', encoding='utf-8') as f:
            yaml.dump(test_config, f, allow_unicode=True)
        
        self.config = Config(self.test_config_file)
    
    def tearDown(self):
        # 删除测试配置文件
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)
    
    def test_get_existing_key(self):
        # 测试获取存在的配置项
        self.assertEqual(self.config.get("test.string"), "value")
        self.assertEqual(self.config.get("test.number"), 123)
        self.assertEqual(self.config.get("test.boolean"), True)
    
    def test_get_nested_key(self):
        # 测试获取嵌套的配置项
        self.assertEqual(self.config.get("test.nested.key"), "nested_value")
    
    def test_get_nonexistent_key(self):
        # 测试获取不存在的配置项
        self.assertIsNone(self.config.get("nonexistent.key"))
        self.assertEqual(self.config.get("nonexistent.key", "default"), "default")
    
    def test_get_wechat_alias(self):
        # 测试获取微信别名配置
        alias_list = self.config.get("wechat.alias")
        self.assertIsNotNone(alias_list)
        self.assertEqual(len(alias_list), 2)
        self.assertEqual(alias_list[0]["wxid"], "wxid_1")
        self.assertEqual(alias_list[0]["alias"], ["爸爸", "康强"])
        self.assertEqual(alias_list[1]["wxid"], "wxid_2")
        self.assertEqual(alias_list[1]["alias"], ["妈妈", "园园"])
    
    def test_file_not_found(self):
        # 测试配置文件不存在的情况
        config = Config("nonexistent_file.yml")
        self.assertIsNone(config.get("any.key"))
        self.assertEqual(config.get("any.key", "default"), "default")
    
    def test_invalid_yaml(self):
        # 测试无效的YAML文件
        invalid_file = "invalid.yml"
        try:
            with open(invalid_file, 'w', encoding='utf-8') as f:
                f.write("invalid: yaml: content:")
            
            config = Config(invalid_file)
            # 即使YAML无效，也应该能够正常工作，只是返回默认值
            self.assertIsNone(config.get("any.key"))
            self.assertEqual(config.get("any.key", "default"), "default")
        finally:
            if os.path.exists(invalid_file):
                os.remove(invalid_file)
    
    def test_get_wechat_alias_method(self):
        # 测试获取微信别名方法
        self.assertEqual(self.config.get_wxid_by_alias("爸爸"), "wxid_1")
        self.assertEqual(self.config.get_wxid_by_alias("康强"), "wxid_1")
        self.assertEqual(self.config.get_wxid_by_alias("妈妈"), "wxid_2")
        self.assertEqual(self.config.get_wxid_by_alias("园园"), "wxid_2")
        self.assertEqual(self.config.get_wxid_by_alias("小明"), "wxid_3")
        self.assertEqual(self.config.get_wxid_by_alias("明明"), "wxid_3")
        
        # 测试不存在的别名
        self.assertIsNone(self.config.get_wxid_by_alias("不存在的别名"))
        
        # 测试配置中不存在contacts的情况
        config_without_contacts = Config("nonexistent_file.yml")
        self.assertIsNone(config_without_contacts.get_wxid_by_alias("任何别名"))


if __name__ == "__main__":
    unittest.main()

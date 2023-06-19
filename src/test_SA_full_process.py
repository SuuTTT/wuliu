# test_SA_full_process.py
import unittest
from unittest.mock import patch
from optimizer import *
from util import *


class TestFullProcess(unittest.TestCase):

    @patch('requests.post')
    def test_full_process(self, mock_post):

        # 创建 Mock 对象以返回预期的响应
        mock_response_inventory = self._mock_response({
            "code": 200,
            "data": [
                {
                    "ckkcsjVOS": [
                        {
                            "sjjd": "2023-06-30T00:00:00",
                            "ckkcvos": [
                                {
                                    "cknm": "WH1",
                                    "xyl": 10.0
                                },
                                {
                                    "cknm": "WH2",
                                    "xyl": 8.0
                                }
                            ]
                        }
                    ],
                    "spnm": "AUX"
                }
            ]
        })
        mock_response_cost = self._mock_response({
            "code": 200,
            "data": 100.0  # 总调配成本
        })
        mock_response_strategy = self._mock_response({
            "code": 200,
            "data": [
                {
                    "cknm": "WH1",
                    "qynm": "company001",
                    "spnm": "AUX",
                    "xqsj": "2023-06-30T00:00:00",
                    "cb": 100.0
                }
            ]
        })
        
        mock_post.side_effect = [mock_response_inventory, mock_response_cost, mock_response_strategy]

        # 测试获取仓库库存
        response = get_warehouse_inventory("AUX", "2023-06-30T00:00:00")
        self.assertEqual(response['code'], 200)
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['data'][0]['spnm'], 'AUX')

        # 测试获取总的调配成本
        response = get_total_dispatch_cost("AUX", "WH1", 117.3, 39.9, 10.0, "kg")
        self.assertEqual(response['code'], 200)
        self.assertEqual(response['data'], 100.0)

        # 测试获取最优调配策略
        response = get_optimal_dispatch_strategy(request_data)
        self.assertEqual(response['code'], 200)
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['data'][0]['cknm'], 'WH1')
        self.assertEqual(response['data'][0]['spnm'], 'AUX')
        self.assertEqual(response['data'][0]['cb'], 100.0)

    def _mock_response(self, response_data):
        mock_resp = unittest.mock.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = response_data
        return mock_resp

if __name__ == '__main__':
    unittest.main()

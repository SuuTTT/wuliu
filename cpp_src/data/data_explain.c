
//"输入":
{
	"spdd":[//商品订单的拼音首字母缩写
		{
			"ddnm":"",//订单内码，内码就是ID
			"qynm":"",//企业内码
			"spnm":"",//商品内码
			"sl":1,   //数量
			"lg":"",  //量纲
			"ckdata":[
				{
					"cknm":"",
					"dwyssj":3.0	//单位运输时间
				},
				{
					"cknm":"",
					"dwyssj":3.0
				}
			]
		},...
	],
	"ck":[
		{"cknm1":
			[{"spnm":"","sl":10,"lg":"枚"},{"spnm":"","sl":10,"lg":"枚"},{"spnm":"","sl":10,"lg":"枚"},{"spnm":"","sl":10,"lg":"枚"}]},
		{"cknm2":
			[{"spnm":"","sl":10,"lg":"枚"},{"spnm":"","sl":10,"lg":"枚"},{"spnm":"","sl":10,"lg":"枚"},{"spnm":"","sl":10,"lg":"枚"}]}
	]
}

//"输出":
{
	"code":200,
	"data":[
		{
			"ddnm":"",
			"cknm":"",
			"qynm":"",
			"spnm":"",
			"sl":1,
			"lg":"枚",
			"dpsj":3.0//调配时间
			//=出库时间（恒为0）+运输时间
		}
	]
}
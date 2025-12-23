# -*- coding: utf-8 -*-
"""
银行交易数据清洗与分析项目
生成模拟数据 -> 数据清洗 -> 基础分析 -> 可视化
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持（可选，如果图表中文显示为方框可忽略）
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("=== 第1步：生成模拟银行交易数据 ===")
# 定义数据
data = {
    '交易ID': range(1001, 1021),  # 20笔交易
    '客户ID': ['C1001', 'C1002', 'C1001', 'C1003', 'C1004', 'C1002', 'C1005', 'C1003', 'C1006', 'C1007',
              'C1008', 'C1004', 'C1009', 'C1010', 'C1005', 'C1001', 'C1006', 'C1011', 'C1002', 'C1003'],
    '交易类型': ['存款', '取款', '转账', '存款', '取款', '转账', '存款', '取款', '存款', '转账',
                '取款', '存款', '转账', '存款', '取款', '转账', '存款', '取款', '存款', '转账'],
    '交易金额': [5000, -2000, -1500, 8000, -500, -3000, 12000, -2200, 6000, -4000,
                -1000, 7000, -2500, 9000, -1200, -3500, 4500, -800, 3000, -1500],
    '交易渠道': ['网银', 'ATM', '手机银行', '柜台', 'ATM', '网银', '手机银行', '柜台', '网银', '手机银行',
                'ATM', '柜台', '网银', '手机银行', 'ATM', '手机银行', '柜台', 'ATM', '网银', '柜台'],
    '交易状态': ['成功', '成功', '成功', '成功', '失败', '成功', '成功', '成功', '成功', '成功',
                '成功', '成功', '成功', '成功', '成功', '成功', '成功', '成功', '成功', '成功']
}

# 创建DataFrame（Pandas的核心数据结构，可以理解为一张Excel表格）
df = pd.DataFrame(data)
print("原始数据预览：")
print(df.head())  # 只显示前5行
print("\n数据基本信息：")
print(df.info())

print("\n=== 第2步：数据清洗 ===")
# 2.1 处理缺失值（我们的模拟数据没有缺失，但这是标准步骤）
print("检查缺失值：")
print(df.isnull().sum())

# 2.2 处理重复值
duplicate_rows = df.duplicated().sum()
print(f"发现重复行数：{duplicate_rows}")
# 如果有重复行，可以用 df = df.drop_duplicates() 删除

# 2.3 处理异常值：这里我们假设交易金额绝对值大于10000或小于-5000为异常
print("\n检查交易金额异常值（>10000或<-5000）：")
abnormal = df[(df['交易金额'] > 10000) | (df['交易金额'] < -5000)]
if not abnormal.empty:
    print(abnormal)
    # 一种处理方式：将这些异常值设为NaN（缺失值），然后可以用中位数填充
    # df.loc[(df['交易金额'] > 10000) | (df['交易金额'] < -5000), ‘交易金额’] = np.nan
    # df[‘交易金额’].fillna(df[‘交易金额’].median(), inplace=True)
else:
    print("未发现定义的异常值。")

# 2.4 数据格式整理：确保金额为数值型，状态为分类变量等（这里已确保）
df['交易类型'] = df['交易类型'].astype('category')
df['交易渠道'] = df['交易渠道'].astype('category')
print("\n清洗后数据类型：")
print(df.dtypes)

print("\n=== 第3步：基础数据分析 ===")
# 3.1 总体统计
print("交易金额统计描述（元）：")
print(df['交易金额'].describe())

# 3.2 按交易类型统计
print("\n按【交易类型】统计（笔数、总额、平均额）：")
type_summary = df.groupby('交易类型')['交易金额'].agg(['count', 'sum', 'mean']).round(2)
print(type_summary)

# 3.3 按交易渠道统计
print("\n按【交易渠道】统计交易笔数：")
channel_count = df['交易渠道'].value_counts()
print(channel_count)

# 3.4 识别失败交易
print("\n失败的交易：")
failed_transactions = df[df['交易状态'] == '失败']
print(failed_transactions)

print("\n=== 第4步：数据可视化 ===")
# 创建两个并排的图表
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 4.1 各交易类型总额柱状图
type_summary['sum'].plot(kind='bar', ax=axes[0], color=['green', 'red', 'orange'])
axes[0].set_title('各交易类型总金额对比')
axes[0].set_ylabel('总金额（元）')
axes[0].tick_params(axis='x', rotation=0)

# 4.2 各渠道交易笔数柱状图
channel_count.plot(kind='bar', ax=axes[1], color='skyblue')
axes[1].set_title('各交易渠道笔数对比')
axes[1].set_ylabel('交易笔数')
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()  # 自动调整子图间距
# 保存图表为图片
plt.savefig('bank_transaction_analysis.png', dpi=300)
print("图表已保存为 ‘bank_transaction_analysis.png‘")
plt.show()  # 显示图表

print("\n=== 项目完成！ ===")
print("已成功完成：1. 数据生成 2. 数据清洗 3. 业务分析 4. 结果可视化")
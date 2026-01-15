import flet as ft
from datetime import datetime
import pandas as pd  # 引入熊猫库处理Excel


def main(page: ft.Page):
    page.title = "渠道返利计算器 v4.0 (最终版)"
    page.window_width = 500
    page.window_height = 750
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "AUTO"

    # --- 1. 定义界面组件 ---

    input_money = ft.TextField(label="请输入业绩金额 (元)", keyboard_type=ft.KeyboardType.NUMBER)

    dropdown_rate = ft.Dropdown(
        label="选择返利点位",
        options=[
            ft.dropdown.Option("0.01", "友情支持 (1%)"),
            ft.dropdown.Option("0.05", "基础返点 (5%)"),
            ft.dropdown.Option("0.10", "初级代理 (10%)"),
            ft.dropdown.Option("0.15", "中级代理 (15%)"),
            ft.dropdown.Option("0.20", "高级合伙人 (20%)"),
            ft.dropdown.Option("0.30", "特约渠道 (30%)"),
            ft.dropdown.Option("0.45", "核心战略 (45%)"),
            ft.dropdown.Option("0.60", "至尊合伙 (60%)"),
        ],
    )

    txt_result = ft.Text(value="等待计算...", size=20, weight="bold", color="blue")

    # 定义表格
    history_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("时间")),
            ft.DataColumn(ft.Text("金额")),
            ft.DataColumn(ft.Text("比例")),
            ft.DataColumn(ft.Text("返利额")),
        ],
        rows=[],
    )

    # 提示框 (SnackBar)
    page.snack_bar = ft.SnackBar(content=ft.Text("导出成功！文件已保存在当前目录"))

    # --- 2. 业务逻辑 ---

    # 存储原始数据的列表，方便导出用
    data_list = []

    def btn_click(e):
        if not input_money.value:
            input_money.error_text = "请输入金额"
            page.update()
            return
        if not dropdown_rate.value:
            dropdown_rate.error_text = "请选择点位"
            page.update()
            return

        input_money.error_text = None
        dropdown_rate.error_text = None

        try:
            money = float(input_money.value)
            rate = float(dropdown_rate.value)
            result = money * rate
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # A. 更新界面结果
            txt_result.value = f"应付: {result:,.2f} 元"

            # B. 更新界面表格 (视觉)
            new_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(now_time.split(" ")[1])),  # 界面只显示时间，不显示日期，省空间
                    ft.DataCell(ft.Text(f"{money:,.0f}")),
                    ft.DataCell(ft.Text(f"{int(rate * 100)}%")),
                    ft.DataCell(ft.Text(f"{result:,.2f}", color="red", weight="bold")),
                ]
            )
            history_table.rows.insert(0, new_row)

            # C. 记录数据到列表 (为了导出Excel)
            # 这里的 append 是加到列表末尾，但我们为了和表格一致，也可以用 insert(0)
            data_list.insert(0, {
                "记录时间": now_time,
                "业绩金额": money,
                "返利点位": f"{int(rate * 100)}%",
                "应付返利": result
            })

            page.update()

        except ValueError:
            input_money.error_text = "数字格式错误"
            page.update()

    def clear_table(e):
        history_table.rows.clear()
        data_list.clear()  # 数据也要清空
        page.update()

    # 导出 Excel 的核心逻辑
    def export_excel(e):
        if not data_list:
            page.snack_bar.content = ft.Text("表格是空的，没东西可导出！")
            page.snack_bar.open = True
            page.update()
            return

        try:
            # 1. 创建 DataFrame
            df = pd.DataFrame(data_list)

            # 2. 生成文件名 (带时间戳，防止重名)
            file_name = f"返利记录_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"

            # 3. 保存
            df.to_excel(file_name, index=False)

            # 4. 提示成功
            page.snack_bar.content = ft.Text(f"成功导出: {file_name}")
            page.snack_bar.open = True
            page.update()

        except Exception as ex:
            page.snack_bar.content = ft.Text(f"导出失败: {str(ex)}")
            page.snack_bar.open = True
            page.update()

    # --- 3. 布局 ---
    page.add(
        ft.Column(
            [
                ft.Text("返利计算器 v4.0", size=30, weight="bold"),
                ft.Divider(),
                input_money,
                dropdown_rate,
                ft.Row(
                    [
                        ft.ElevatedButton("计算并记录", on_click=btn_click, bgcolor="blue", color="white"),
                        ft.OutlinedButton("清空", on_click=clear_table),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                # 新增：导出按钮
                ft.ElevatedButton("导出为 Excel", on_click=export_excel, icon=ft.Icons.SAVE_ALT, bgcolor="green",
                                  color="white"),

                ft.Divider(),
                txt_result,
                ft.Divider(),
                history_table,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


ft.app(target=main)

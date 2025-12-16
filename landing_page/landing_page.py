import reflex as rx

class State(rx.State):
    """这里管理页面的状态"""
    def sign_up(self):
        return rx.window_alert("🎉 报名通道即将开启，敬请期待！")

# --- 组件部分 ---

def navbar():
    return rx.hstack(
        rx.text("🚀 2025 Python 峰会", font_size="1.5em", font_weight="bold"),
        rx.spacer(),
        rx.button("立即报名", on_click=State.sign_up, color_scheme="red", cursor="pointer"),
        width="100%",
        padding="1em",
        position="sticky",
        top="0",
        z_index="100",
        background_color="white",
        box_shadow="0 2px 4px rgba(0,0,0,0.1)",
    )

def hero_banner():
    return rx.center(
        rx.vstack(
            rx.heading("2025 年度开发者盛典", size="9", color="white", text_align="center"),
            rx.text("吉隆坡 · 12月20日 · 探索 AI 与未来", color="white", font_size="1.5em", text_align="center"),
            rx.button("查看详情", size="4", color_scheme="yellow", margin_top="1em", on_click=State.sign_up, cursor="pointer"),
            align="center",
            spacing="5",
            padding="2em",
        ),
        # 这里暂时用网络图片作为 Banner，后面教你换成自己的
        background_image="url('/banner.png')",
        background_size="cover",
        background_position="center",
        height="60vh",
        width="100%",
    )

def details():
    return rx.container(
        rx.heading("活动亮点", margin_bottom="1em"),
        rx.text("这是一个汇聚全球顶尖开发者的盛会，我们将深入探讨 Python 3.14 新特性、AI Agent 开发以及 Web 全栈技术。", margin_bottom="2em", line_height="1.6"),
        rx.grid(
            rx.card(rx.vstack(rx.icon("calendar"), rx.text("📅 时间: 2025/12/20"))),
            rx.card(rx.vstack(rx.icon("map-pin"), rx.text("📍 地点: Grand Hyatt KL"))),
            rx.card(rx.vstack(rx.icon("gift"), rx.text("🎁 包含: 午餐与精美周边"))),
            columns="3",
            spacing="4",
            width="100%"
        ),
        padding_y="4em",
    )

def tnc():
    return rx.container(
        rx.heading("条款与细则 (TnC)", size="4", margin_bottom="1em"),
        rx.accordion.root(
            rx.accordion.item(header="1. 退款政策", content="门票一经售出，非活动取消原因概不退换。"),
            rx.accordion.item(header="2. 入场须知", content="请携带电子门票（QR Code）在签到处核销入场。"),
            rx.accordion.item(header="3. 肖像权", content="活动现场会有摄影摄像，参与即代表同意主办方使用相关素材。"),
            variant="outline",
            width="100%",
            color_scheme="gray"
        ),
        margin_bottom="4em"
    )

def footer():
    return rx.center(
        rx.text("© 2025 Landing Page Event. All rights reserved.", font_size="0.8em", color="gray"),
        padding="2em",
        background_color="#f5f5f5",
        width="100%"
    )

def index():
    return rx.box(
        navbar(),
        hero_banner(),
        details(),
        rx.divider(),
        tnc(),
        footer(),
        font_family="system-ui"
    )

# --- 启动配置 ---
app = rx.App()
app.add_page(index)
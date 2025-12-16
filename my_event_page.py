import reflex as rx

class State(rx.State):
    """状态管理"""
    def sign_up(self):
        return rx.window_alert("报名通道尚未开启，请稍后！")

# 1. 顶部导航栏
def navbar():
    return rx.hstack(
        rx.text("🚀 MyEvent", font_size="1.5em", font_weight="bold"),
        rx.spacer(),
        rx.button("立即报名", on_click=State.sign_up, color_scheme="red"),
        width="100%",
        padding="1em",
        position="sticky",
        top="0",
        z_index="100",
        background_color="white",
        box_shadow="0 2px 4px rgba(0,0,0,0.1)",
    )

# 2. Hero Banner (带背景图)
def hero_banner():
    return rx.center(
        rx.vstack(
            rx.heading("2025 年度发布会", size="9", color="white"),
            rx.text("吉隆坡 · 12月20日 · 探索未来", color="white", font_size="1.5em"),
            rx.button("查看详情", size="4", color_scheme="yellow", margin_top="1em"),
            align="center",
            spacing="5",
        ),
        # 这里你可以换成网上的图片链接，或者放入 assets 文件夹
        background_image="linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1540575467063-178a50c2df87')",
        background_size="cover",
        background_position="center",
        height="500px",
        width="100%",
    )

# 3. 活动详情
def details():
    return rx.container(
        rx.heading("活动亮点", margin_bottom="1em"),
        rx.text("这里是活动的详细介绍。我们将邀请行业大咖进行分享...", margin_bottom="2em"),
        rx.grid(
            rx.card(rx.text("📅 时间: 2025/12/20")),
            rx.card(rx.text("📍 地点: KLCC")),
            rx.card(rx.text("🎁 包含午餐与礼品")),
            columns="3",
            spacing="4",
            width="100%"
        ),
        padding_y="4em",
    )

# 4. TnC 条款
def tnc():
    return rx.container(
        rx.heading("条款与细则 (TnC)", size="4", margin_bottom="1em"),
        rx.accordion.root(
            rx.accordion.item(header="退款政策", content="门票售出不退不换。"),
            rx.accordion.item(header="隐私声明", content="我们不会泄露您的个人信息。"),
            variant="outline",
            width="100%"
        ),
        margin_bottom="4em"
    )

# 5. 组合页面
def index():
    return rx.box(
        navbar(),
        hero_banner(),
        details(),
        rx.divider(),
        tnc(),
        font_family="system-ui" # 修复字体问题
    )

# 启动应用
app = rx.App()
app.add_page(index)
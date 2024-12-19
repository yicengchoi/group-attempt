import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from card_info import card_data
import requests
import json
import tkinter.font as tkfont
import os
from pygame import mixer
import pygame


class TarotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Reader")
        self.root.geometry("1400x900")  # 页面大小

        # 初始化变量
        self.click_count = 0
        self.selected_images = {}  # 存储每个主题最后一次选择的卡牌索引
        self.current_selected_card = None  # 当前被选择的卡牌
        self.detail_window_open = False  # 标记是否有卡牌详细信息弹窗打开
        self.is_muted = False  # 静音状态变量

        # 每个主题名称
        self.themes = ["Emotions", "Forgot", "Wish"]

        # 卡牌正面和背面图片路径预设
        self.front_images = [
            "theme1_front.jpg",
            "theme2_front.jpg",
            "theme3_front.jpg",
        ]  # 正面图片路径
        self.back_images = [
            "theme1_back.png",
            "theme2_back.png",
            "theme3_back.png",
        ]  # 背面图大图路径

        # 获取当前脚本文件所在目录
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 设置图片目录的相对路径
        self.image_directory = os.path.join(base_dir,'images', 'cards')

        # 创建页面容器
        self.pages = []
        for i in range(3):
            frame = tk.Frame(self.root)
            self.create_page(
                frame, self.themes[i], self.back_images[i]
            )
            self.pages.append(frame)

        # 创建第四页用于显示选择的卡牌
        summary_page = tk.Frame(self.root)
        self.create_summary_page(summary_page)
        self.pages.append(summary_page)

        # 显示第一页
        self.pages[0].pack(fill="both", expand=True)

        # 初始化 pygame 音乐模块
        pygame.mixer.init()
        self.play_background_music()

    def play_background_music(self):
        # 加载并播放背景音乐
        pygame.mixer.music.load("audio/background.mp3")
        pygame.mixer.music.play(-1)  # -1 表示循环播放

    def create_page(self, frame, theme, back_image_path):
        # 设置框架背景为黑色
        frame.config(bg='black')

        # 加载并显标题和主题的图片
        base_dir = os.path.dirname(os.path.abspath(__file__))
        header_image_path = os.path.join(base_dir, 'images', 'button', 'memoryreader.png')
        header_image = Image.open(header_image_path)
        header_image_resized = header_image.resize((380, 65), Image.LANCZOS)
        header_image_tk = ImageTk.PhotoImage(header_image_resized)

        header_label = tk.Label(
            frame, image=header_image_tk, bg='black'  # 设置标签背景为黑色
        )
        header_label.image = header_image_tk
        header_label.pack(pady=20)
        # 创建一个新的框架用于放置按钮
        button_frame = tk.Frame(frame, bg='black')
        button_frame.pack(pady=0, fill='x', expand=True)

        # 加载并缩小下一页按钮图片
        base_dir = os.path.dirname(os.path.abspath(__file__))
        next_button_image_path = os.path.join(base_dir, 'images', 'button', 'next_button.png')
        original_image = Image.open(next_button_image_path)
        resized_image = original_image.resize((80, 35), Image.LANCZOS)
        next_button_image = ImageTk.PhotoImage(resized_image)

        # 创建带图片的 Next 按钮
        next_button = tk.Button(
            button_frame, image=next_button_image, command=self.next_page, bg='black', borderwidth=0
        )
        next_button.image = next_button_image  # 防止图片被垃圾回收
        next_button.pack(side=tk.RIGHT, padx=80, pady=3)

        # 加载并显示静音按钮图
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            mute_image_path = os.path.join(base_dir,'images', 'button', 'mute.png')
            mute_image = Image.open(mute_image_path)
            mute_image_resized = mute_image.resize((35, 35), Image.LANCZOS)
            mute_image_tk = ImageTk.PhotoImage(mute_image_resized)

            # 创建带图片的静音按钮
            mute_button = tk.Button(
                button_frame, image=mute_image_tk, command=self.toggle_mute, bg='black', borderwidth=0
            )
            mute_button.image = mute_image_tk  # 防止图片被垃圾回收
            mute_button.pack(side=tk.RIGHT, padx=5, pady=3)
        except Exception as e:
            print(f"Error loading mute image: {e}")

        # 插入新的线条图片
        base_dir = os.path.dirname(os.path.abspath(__file__))
        line_image_path = os.path.join(base_dir, 'images', 'button', 'line.png')
        line_image = Image.open(line_image_path)
        line_image_resized = line_image.resize((1220, 3), Image.LANCZOS)
        line_image_tk = ImageTk.PhotoImage(line_image_resized)

        line_label = tk.Label(
            frame, image=line_image_tk, bg='black'
        )
        line_label.image = line_image_tk
        line_label.pack(pady=0, fill='x', expand=True)

        # 插入新的选择图片
        base_dir = os.path.dirname(os.path.abspath(__file__))
        choose_image_path = os.path.join(base_dir,'images', 'button', 'choose.png')
        choose_image = Image.open(choose_image_path)
        choose_image_resized = choose_image.resize((450, 15), Image.LANCZOS)
        choose_image_tk = ImageTk.PhotoImage(choose_image_resized)

        choose_label = tk.Label(
            frame, image=choose_image_tk, bg='black'
        )
        choose_label.image = choose_image_tk
        choose_label.pack(pady=0)

        # 创建卡牌网格
        grid_frame = tk.Frame(frame, bg='black')
        grid_frame.pack(pady=5)

        # 加载背面图片并分割
        back_image = Image.open(back_image_path).resize((960, 480))  # 假设为960x480
        card_size = 120  # 单张卡片大小
        back_images = [
            back_image.crop(
                (
                    (i % 8) * card_size,  # 左
                    (i // 8) * card_size,  # 上
                    ((i % 8) + 1) * card_size,  # 右
                    ((i // 8) + 1) * card_size,  # 下
                )
            )
            for i in range(32)
        ]

        for i in range(32):  # 每个主题有31张图片
            # 根据主题和索引生成正面图片路径
            front_image_path = os.path.join(self.image_directory, f'{theme.lower()}_{i + 1}.jpg')

            # 检查图片是否存在
            if not os.path.exists(front_image_path):
                print(f"Image not found: {front_image_path}")
                continue

            # 加载正面图
            front_image = Image.open(front_image_path).resize((card_size, card_size))
            front_photo = ImageTk.PhotoImage(front_image)
            back_photo = ImageTk.PhotoImage(back_images[i])

            # 创建卡牌
            card_label = tk.Label(
                grid_frame,
                image=back_photo,
                bg="black",
                relief="flat",
                highlightthickness=0,
                width=card_size,
                height=card_size,
            )
            card_label.image = back_photo  # 保持引用
            card_label.grid(row=i // 8, column=i % 8, padx=5, pady=5)

            # 卡牌翻转点击事件
            card_label.bind(
                "<Button-1>",
                lambda e, idx=i, lbl=card_label, front=front_photo, back=back_photo, theme=theme: self.show_card_detail(
                    idx, lbl, front, back, theme
                ),
            )

    def create_summary_page(self, frame):
        """创建选择摘要页面"""
        frame.config(bg='black')  # 设置背景为黑色

        # 加载并调整标题图片的尺寸
        title_image_path = r"images/button/title4.png"
        title_image = Image.open(title_image_path).resize((550, 80))  # 调整尺寸
        title_photo = ImageTk.PhotoImage(title_image)

        title_label = tk.Label(frame, image=title_photo, bg='black')
        title_label.image = title_photo  # 保持引用
        title_label.pack(pady=20)

        # 显示选择结果
        self.summary_frame = tk.Frame(frame, bg='black')  # 用于显示选中卡片的框架
        self.summary_frame.pack(pady=20)

        # 按钮框架
        button_frame = tk.Frame(frame, bg='black')  # 设置按钮框架背景为黑色
        button_frame.pack(pady=20)

        # 加载并调整 Prophecy of Memory 按钮图片的尺寸
        prophecy_image_path = r"images/button/pro.png"
        prophecy_image = Image.open(prophecy_image_path).resize((230, 35))  # 调整尺寸
        prophecy_photo = ImageTk.PhotoImage(prophecy_image)

        prophecy_button = tk.Button(
            button_frame,
            image=prophecy_photo,
            command=self.show_prophecy,
            bg='black', borderwidth=0  # 设置按钮背景和边框
        )
        prophecy_button.image = prophecy_photo  # 保持引用
        prophecy_button.pack(side="left", padx=10)

        # 加载并调整 Restart 按钮图片的尺寸
        restart_image_path = r"images/button/restart.png"
        restart_image = Image.open(restart_image_path).resize((100, 35))  # 调整尺寸
        restart_photo = ImageTk.PhotoImage(restart_image)

        back_button = tk.Button(
            button_frame,
            image=restart_photo,
            command=self.restart,
            bg='black', borderwidth=0  # 设置按钮背景和边框
        )
        back_button.image = restart_photo  # 保持引用
        back_button.pack(side="left", padx=10)

    def show_card_detail(self, idx, label, front_photo, back_photo, theme):
        """展示卡牌细节并记录选择"""
        if self.current_selected_card:
            self.current_selected_card.config(image=self.current_selected_card_back)
            self.current_selected_card.image = self.current_selected_card_back

        if label.image == back_photo:
            label.config(image=front_photo)
            label.image = front_photo
            self.current_selected_card = label
            self.current_selected_card_back = back_photo
            self.selected_images[theme] = idx

            # 如果已经有打开的窗口，先关闭它
            if self.detail_window_open:
                for widget in self.root.winfo_children():
                    if isinstance(widget, tk.Toplevel):
                        widget.destroy()
                self.detail_window_open = False

            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Card Detail - {theme}")
            detail_window.geometry("500x600")
            detail_window.config(bg='black')  # 设置背景为黑色

            # 确保窗口总是在最前面
            detail_window.lift()
            detail_window.focus_force()

            # 标记弹窗已打开
            self.detail_window_open = True

            card_detail_label = tk.Label(
                detail_window, image=front_photo, bg="black"
            )
            card_detail_label.image = front_photo
            card_detail_label.pack(pady=20)

            # Fetch the correct quote based on the theme and index
            quote = card_data.get(theme, {}).get(idx, {}).get('quote', 'No quote available.')

            # Debug line to check if the quote is being fetched correctly
            print(f"Quote: {quote}")  # Debug line

            text_label = tk.Label(
                detail_window,
                text=quote,
                font=("Courier New", 16, "bold"),  # 设置字体为加粗
                wraplength=350,
                bg='black',
                fg='white'
            )
            text_label.pack()

            # 加载并调整 "Seclet" 按钮图片的尺寸
            seclet_image_path = r"images/button/seclet.png"
            seclet_image = Image.open(seclet_image_path).resize((100, 35))  # 调整尺寸
            seclet_photo = ImageTk.PhotoImage(seclet_image)

            # 使用图片创建按钮
            close_button = tk.Button(
                detail_window,
                image=seclet_photo,
                command=lambda: self.close_detail_window(detail_window),
                bg='black', borderwidth=0  # 设置按钮背景和边框
            )
            close_button.image = seclet_photo  # 保持引用
            close_button.pack(pady=20)

    def close_detail_window(self, detail_window):
        """关卡牌详细信息弹窗"""
        self.detail_window_open = False  # 先重置标志位
        detail_window.destroy()

    def next_page(self):
        """切换到下一页"""
        if self.click_count < len(self.pages) - 1:
            self.pages[self.click_count].pack_forget()
            self.click_count += 1
            self.pages[self.click_count].pack(fill="both", expand=True)

        # 如果是最后一页，更新选择摘要
        if self.click_count == len(self.pages) - 1:
            self.update_summary()

    def update_summary(self):
        """更新选择摘要"""
        # 清除之前的内容
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        for theme, idx in self.selected_images.items():
            # 加载选中卡片的正面图片
            front_image_path = os.path.join(self.image_directory, f'{theme.lower()}_{idx + 1}.jpg')
            if os.path.exists(front_image_path):
                front_image = Image.open(front_image_path).resize((120, 120))
                front_photo = ImageTk.PhotoImage(front_image)

                # 显示卡片图片
                card_label = tk.Label(self.summary_frame, image=front_photo, bg='black')
                card_label.image = front_photo  # 保持引用
                card_label.pack(side="left", padx=10)

                # 显示卡片对应的文字
                quote = card_data.get(theme, {}).get(idx, {}).get('quote', 'No quote available.')
                text_label = tk.Label(self.summary_frame, text=quote, font=("Calibri", 14), wraplength=200, bg='black',
                                      fg='white')
                text_label.pack(side="left", padx=10)

    def restart(self):
        """重新开始"""
        self.pages[self.click_count].pack_forget()
        self.click_count = 0
        self.selected_images = {}
        self.current_selected_card = None
        self.pages[0].pack(fill="both", expand=True)

    def make_rounded_corner(self, img):
        """返回原始图像，不进行圆角处理"""
        return img

    def generate_prophecy(self):
        """生成预言诗句"""
        try:
            # 检查LM Studio服务是否运行
            try:
                response = requests.get('http://localhost:1234/v1/models')
                if response.status_code != 200:
                    return "Error: LM Studio server is not running properly. Please start the server in LM Studio."
            except requests.exceptions.ConnectionError:
                return "Error: Cannot connect to LM Studio server. Please ensure LM Studio is running and the server is started."

            # 收集所有选中卡片的引用
            selected_quotes = []
            for theme, idx in self.selected_images.items():
                quote = card_data.get(theme, {}).get(idx, {}).get('quote', '')
                if quote:
                    selected_quotes.append(quote)

            if not selected_quotes:
                return "No cards selected to generate prophecy."

            # 准备提示词
            messages = [
                {"role": "system", "content": """You are a wise prophet who creates meaningful prophecies based on memory fragments. 
                Create poetic prophecies that reflect deep insights about life and memories.
                Do not include pronunciation guides or translation notes."""},
                {"role": "user", "content": f"""Based on these memory fragments:
                {' '.join(selected_quotes)}

                Create a poetic prophecy following these rules:
                1. One English title and 4-6 lines of English poetry
                2. One Chinese title and 4-6 lines of Chinese poetry
                3. Capture the essence and emotions of the memory fragments
                4. Offer wisdom and insight about the future
                5. Do not include pronunciation,translation notes or asterisks

                Format exactly as:
                [English Title]
                [English verses]

                [Chinese Title]
                [Chinese verses]"""}
            ]

            # 调用API时添加超时设置
            response = requests.post(
                'http://localhost:1234/v1/chat/completions',
                headers={'Content-Type': 'application/json'},
                json={
                    "model": "meta-llama-3.1-8b-instruct",
                    "messages": messages,
                    "temperature": 0.8,
                    "max_tokens": 800,
                    "top_p": 0.9,
                    "frequency_penalty": 0.3,
                    "presence_penalty": 0.3
                },
                timeout=30  # 添加30秒超时
            )

            if response.status_code == 200:
                # 打印完整的响应内容以调试
                print("API Response:", response.json())

                prophecy = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                if not prophecy:
                    return "Error: No prophecy was generated. Please try again."
                return prophecy
            elif response.status_code == 404:
                return "Error: Model not found. Please ensure the correct model is loaded in LM Studio."
            else:
                return f"Error: Failed to generate prophecy. Status code: {response.status_code}"

        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error connecting to LM Studio: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def show_prophecy(self):
        """显示预言诗句的弹窗"""

        def get_font_with_fallback(font_name, size=14):
            """获取字体，如果指定字体不可用则使用回退体"""
            try:
                available_fonts = tkfont.families()  # 使用正确的tkfont引用

                # 更新字体回退顺序
                font_fallbacks = {
                    'Calibri': ['Arial', 'Helvetica', 'MS Sans Serif'],  # 英文字体回退
                    'Microsoft YaHei': ['微软雅黑', 'SimHei', 'SimSun']  # 中文字体回退
                }

                # 检查请求的字体及其回退选项
                fallback_options = font_fallbacks.get(font_name, [])
                for font in [font_name] + fallback_options:
                    if font in available_fonts:
                        return (font, size)

                # 如果所有回退选项都不可用，返回系统默认字体
                return ('TkDefaultFont', size)
            except Exception as e:
                print(f"Font loading error: {e}")

        try:
            prophecy_window = tk.Toplevel(self.root)
            prophecy_window.title("Prophecy of Memory")
            prophecy_window.geometry("640x700")
            prophecy_window.config(bg='black')

            # 加载并调整标题图片的尺寸
            base_dir = os.path.dirname(os.path.abspath(__file__))
            title_image_path = os.path.join(base_dir, 'images', 'button', 'lmtitle.png')
            title_image = Image.open(title_image_path).resize((400, 60))  # 调整尺寸以缩小图片
            title_photo = ImageTk.PhotoImage(title_image)

            # 使用图片创建标题标签
            title_label = tk.Label(prophecy_window, image=title_photo, bg='black')
            title_label.image = title_photo  # 保持引用
            title_label.pack(pady=10)  # 添加一些垂直间距

            # 使用try-except包装字体设置
            try:
                loading_font = get_font_with_fallback('Calibri')
                loading_label = tk.Label(
                    prophecy_window,
                    text="Generating prophecy...",
                    font=loading_font,
                    bg='black',  # 设置背景为白色
                    fg='whit',  # 设置文本为黑色
                    justify='center'  # 文本居中
                )
            except Exception as e:
                print(f"Loading font error: {e}")  # 添加错误日志
                loading_label = tk.Label(
                    prophecy_window,
                    text="Generating prophecy...",
                    bg='black',
                    fg='white',
                    justify='center'
                )

            loading_label.pack(pady=20)
            prophecy_window.update()

            # 生成预言
            prophecy_text = self.generate_prophecy()
            loading_label.destroy()

            # 创建文本显示区域
            text_frame = tk.Frame(prophecy_window)
            text_frame.pack(pady=20, expand=True, fill="both")

            # 加载背景图片
            base_dir = os.path.dirname(os.path.abspath(__file__))
            bg_image_path = os.path.join(base_dir, 'images', 'bg', 'text.png')
            bg_image = Image.open(bg_image_path)
            bg_photo = ImageTk.PhotoImage(bg_image)

            # 使用标签显示背景图片
            bg_label = tk.Label(text_frame, image=bg_photo)
            bg_label.image = bg_photo  # 保持引用
            bg_label.place(relwidth=1, relheight=1)  # 调整标签大小以填充框架

            text_widget = tk.Text(
                text_frame,
                wrap="word",
                width=40,
                height=15,
                relief="flat",
                borderwidth=0,
                # 设置背景为白色
                fg='black'  # 设置文本为黑色
            )
            text_widget.pack(padx=20, expand=True, fill="both")

            # 获取更新后的英文和中文字体
            en_font = get_font_with_fallback('Calibri')
            cn_font = get_font_with_fallback('Microsoft YaHei')

            # 配置字体标签
            text_widget.tag_configure("en_text", font=en_font, justify='center', spacing1=2, spacing3=2)  # 缩小行距
            text_widget.tag_configure("cn_text", font=cn_font, justify='center')

            # 处理预言文本
            lines = prophecy_text.split('\n')
            is_english_section = True  # 跟踪当前处理的是否为英文部分
            skip_line = False  # 用于跳过注释

            for line in lines:
                # 跳过空行、注释和拼音
                if (not line.strip() or
                        line.startswith('(Note:') or
                        line.startswith('(Mòu') or
                        '**' in line):  # 跳过带**的行
                    continue

                # 移除多余的符号
                line = line.strip('()*\n')

                # 检查是否包含中文字符
                has_chinese = any('\u4e00' <= char <= '\u9fff' for char in line)

                if has_chinese:
                    # 中文部分
                    if len(line.strip()) <= 20:  # 标题
                        text_widget.insert("end", line + "\n\n", "cn_title")
                    else:  # 诗句内容
                        text_widget.insert("end", line + "\n", "cn_text")
                else:
                    # 英文部分
                    if len(line.strip()) <= 50:  # 标题
                        text_widget.insert("end", line + "\n\n", "en_title")
                    else:  # 诗句内容
                        text_widget.insert("end", line + "\n", "en_text")

            # 配置不同的字体样式
            text_widget.tag_configure("en_title", font=get_font_with_fallback('Courier New', 14), justify='center',
                                      spacing1=1, spacing3=1)
            text_widget.tag_configure("cn_title", font=get_font_with_fallback('宋体', 14), justify='center', spacing1=1,
                                      spacing3=1)
            text_widget.tag_configure("en_text", font=get_font_with_fallback('Courier New', 12), justify='center',
                                      spacing1=1, spacing3=1)
            text_widget.tag_configure("cn_text", font=get_font_with_fallback('宋体', 12), justify='center', spacing1=1,
                                      spacing3=1)

            # 设置为只读
            text_widget.configure(state="disabled")

            # 加载并调整 Close 按钮图片的尺寸
            base_dir = os.path.dirname(os.path.abspath(__file__))
            close_image_path = os.path.join(base_dir, 'images', 'button', 'close.png')
            close_image = Image.open(close_image_path).resize((75, 30))  # 调整尺寸
            close_photo = ImageTk.PhotoImage(close_image)

            # 使用图片创建关闭按钮
            close_button = tk.Button(
                prophecy_window,
                image=close_photo,
                command=prophecy_window.destroy,
                bg='black', borderwidth=0  # 设置按钮背景和边框
            )
            close_button.image = close_photo  # 保持引用
            close_button.pack(pady=10)
        except Exception as e:
            print(f"Error showing prophecy: {e}")

    def toggle_mute(self):
        """切换静音状态"""
        if self.is_muted:
            pygame.mixer.music.unpause()
            print("Unmuted")
        else:
            pygame.mixer.music.pause()
            print("Muted")
        self.is_muted = not self.is_muted


def main():
    root = tk.Tk()
    app = TarotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


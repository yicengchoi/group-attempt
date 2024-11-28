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
        self.is_playing = False
        self.volume = 0.5  # 默认音量

        # 初始化音乐播放器
        pygame.mixer.init()
        self.setup_background_music()

        # 创建音量控制按钮
        self.create_volume_control()

        # 每个主题名称
        self.themes = ["Emotions", "Forgot", "Wish"]

        # 卡牌正面和背面图片路径预设
        self.front_images = [
            "theme1_front.jpg",
            "theme2_front.jpg",
            "theme3_front.jpg",
        ]  # 正面图片路径
        self.back_images = [
            "theme1_back.jpg",
            "theme2_back.jpg",
            "theme3_back.jpg",
        ]  # 背面图大图路径

        # 获取当前脚本文件所在目录
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 设置图片目录的相对路径
        self.image_directory = os.path.join(base_dir, '..', '..', 'images', 'cards')

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

    def create_page(self, frame, theme, back_image_path):
        # 创建标题
        title_label = tk.Label(
            frame, text="Memory Reader", font=("Calibri", 24, "bold"), pady=20
        )
        title_label.pack()

        # 显示主题和下一页按钮
        theme_frame = tk.Frame(frame)
        theme_frame.pack(pady=10, anchor="w", fill="x")

        theme_label = tk.Label(
            theme_frame, text=f"Theme: {theme}", font=("Calibri", 18), anchor="w"
        )
        theme_label.pack(side="left", padx=20)

        next_button = tk.Button(
            theme_frame,
            text="Next",
            font=("Arial", 14),
            command=self.next_page,
        )
        next_button.pack(side="right", padx=20)

        # 创建卡牌网格
        grid_frame = tk.Frame(frame)
        grid_frame.pack(pady=20)

        # 加载背面图片并分割
        back_image = Image.open(back_image_path).resize((960, 480))  # 假设为960x480
        card_size = 120  # 单张卡片大小
        back_images = [
            self.make_rounded_corner(
                back_image.crop(
                    (
                        (i % 8) * card_size,  # 左
                        (i // 8) * card_size,  # 上
                        ((i % 8) + 1) * card_size,  # 右
                        ((i // 8) + 1) * card_size,  # 下
                    )
                )
            )
            for i in range(32)
        ]

        for i in range(32):  # 每个主题有31张图片
            # 根据主题和索引生成正面图片路径
            front_image_path = os.path.join(self.image_directory, f'{theme.lower()}_{i+1}.jpg')
            
            # 检查图片是否存在
            if not os.path.exists(front_image_path):
                print(f"Image not found: {front_image_path}")
                continue

            # 加载正面图片
            front_image = self.make_rounded_corner(
                Image.open(front_image_path).resize((card_size, card_size))
            )
            front_photo = ImageTk.PhotoImage(front_image)
            back_photo = ImageTk.PhotoImage(back_images[i])

            # 创建卡牌
            card_label = tk.Label(
                grid_frame,
                image=back_photo,
                bg="white",
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
        title_label = tk.Label(
            frame, text="Your Selected Cards", font=("Calibri", 24, "bold"), pady=20
        )
        title_label.pack()

        # 显示选择结果
        self.summary_label = tk.Label(
            frame, text="", font=("Calibri", 18), justify="left", pady=20
        )
        self.summary_label.pack()

        # 按钮框架
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)

        # 预言按钮
        prophecy_button = tk.Button(
            button_frame,
            text="Prophecy of Memory",
            font=("Calibri", 14),
            command=self.show_prophecy,
        )
        prophecy_button.pack(side="left", padx=10)

        # 返回按钮
        back_button = tk.Button(
            button_frame,
            text="Restart",
            font=("Calibri", 14),
            command=self.restart,
        )
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
            detail_window.geometry("400x400")
            
            # 确保窗口总是在最前面
            detail_window.lift()
            detail_window.focus_force()

            # 标记弹窗已打开
            self.detail_window_open = True
            
            card_detail_label = tk.Label(
                detail_window, image=front_photo, bg="white"
            )
            card_detail_label.image = front_photo
            card_detail_label.pack(pady=20)

            # Fetch the correct quote based on the theme and index
            quote = card_data.get(theme, {}).get(idx, {}).get('quote', 'No quote available.')

            # Debug line to check if the quote is being fetched correctly
            print(f"Quote: {quote}")  # Debug line

            text_label = tk.Label(
                detail_window, text=quote, font=("Calibri", 16), wraplength=350
            )
            text_label.pack()

            close_button = tk.Button(
                detail_window,
                text="Seclet",
                command=lambda: self.close_detail_window(detail_window),
            )
            close_button.pack(pady=20)

    def close_detail_window(self, detail_window):
        """关闭卡牌详细信息弹窗"""
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
        summary_text = "You have selected:\n"
        for theme, idx in self.selected_images.items():
            summary_text += f" - {theme} card {idx + 1}\n"
        self.summary_label.config(text=summary_text)

    def restart(self):
        """重新开始"""
        self.pages[self.click_count].pack_forget()
        self.click_count = 0
        self.selected_images = {}
        self.current_selected_card = None
        self.pages[0].pack(fill="both", expand=True)

    def make_rounded_corner(self, img):
        """将图片处理为圆角"""
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            [(0, 0), img.size], radius=20, fill=255  # 圆角半径
        )
        img.putalpha(mask)
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
            """获取字体，如果指定字体不可用则使用回退字体"""
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
            prophecy_window.geometry("600x400")
            
            # 使用try-except包装字体设置
            try:
                loading_font = get_font_with_fallback('Calibri')
                loading_label = tk.Label(
                    prophecy_window, 
                    text="Generating prophecy...", 
                    font=loading_font
                )
            except Exception as e:
                print(f"Loading font error: {e}")  # 添加错误日志
                loading_label = tk.Label(
                    prophecy_window, 
                    text="Generating prophecy..."
                )
            
            loading_label.pack(pady=20)
            prophecy_window.update()
            
            # 生成预言
            prophecy_text = self.generate_prophecy()
            loading_label.destroy()
            
            # 创建文本显示区域
            text_frame = tk.Frame(prophecy_window)
            text_frame.pack(pady=20, expand=True, fill="both")
            
            text_widget = tk.Text(
                text_frame,
                wrap="word",
                width=40,
                height=15,
                relief="flat",
                borderwidth=0
            )
            text_widget.pack(padx=20, expand=True, fill="both")
            
            # 获取更新后的英文和中文字体
            en_font = get_font_with_fallback('Calibri')
            cn_font = get_font_with_fallback('Microsoft YaHei')
            
            # 配置字体标签
            text_widget.tag_configure("en_text", font=en_font)
            text_widget.tag_configure("cn_text", font=cn_font)
            
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
            text_widget.tag_configure("en_title", font=get_font_with_fallback('Calibri', 16))
            text_widget.tag_configure("cn_title", font=get_font_with_fallback('Microsoft YaHei', 16))
            text_widget.tag_configure("en_text", font=get_font_with_fallback('Calibri', 14))
            text_widget.tag_configure("cn_text", font=get_font_with_fallback('Microsoft YaHei', 14))
            
            # 设置为只读
            text_widget.configure(state="disabled")
            
            # 关闭按钮使用新的英文字体
            close_button = tk.Button(
                prophecy_window,
                text="Close",
                font=get_font_with_fallback('Calibri', 12),
                command=prophecy_window.destroy
            )
            close_button.pack(pady=10)
        except Exception as e:
            print(f"Error showing prophecy: {e}")

    def setup_background_music(self):
        """设置背景音乐"""
        try:
            music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'audio', 'background.mp3')
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)  # -1表示循环播放
            self.is_playing = True
        except Exception as e:
            print(f"无法加载背景音乐: {e}")

    def create_volume_control(self):
        """创建音量控制按钮"""
        # 创建一个框架，放在主窗口的左上角
        self.volume_frame = tk.Frame(self.root, bg='white')  # 添加背景色以便于调试
        self.volume_frame.pack(side="top", anchor="nw", padx=10, pady=10)
        
        # 音量按钮
        self.volume_button = tk.Button(
            self.volume_frame,
            text="🔊",
            font=("Calibri", 12),
            command=self.toggle_music,
            width=2,  # 设置按钮宽度
            height=1  # 设置按钮高度
        )
        self.volume_button.pack(side="left", padx=5)
        
        # 音量滑块
        self.volume_slider = tk.Scale(
            self.volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            length=100,  # 设置滑块长度
            command=self.change_volume
        )
        self.volume_slider.set(self.volume * 100)
        self.volume_slider.pack(side="left", padx=5)

    def toggle_music(self):
        """切换音乐播放状态"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.volume_button.config(text="🔈")
        else:
            pygame.mixer.music.unpause()
            self.volume_button.config(text="🔊")
        self.is_playing = not self.is_playing

    def change_volume(self, value):
        """调整音量"""
        self.volume = float(value) / 100
        pygame.mixer.music.set_volume(self.volume)

def main():
    root = tk.Tk()
    app = TarotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

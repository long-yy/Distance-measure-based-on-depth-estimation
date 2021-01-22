from PIL import Image, ImageTk
import windnd


import tkinter as tk
from tkinter import ttk


def show_input(files):
    """
    获得拖拽图片的路径并展示
    输入：拖拽的文件列表file
    """
    filepath = files[0].decode('gbk')    # 获取列表中的第一个文件路径(拖动多个文件时只获取第一个）
    image_open = Image.open(filepath)   # 加载图片
    image_resize = image_open.resize((width, height))   # 缩放图片
    image = ImageTk.PhotoImage(image_resize)    # 利用PIL包转化tkinter兼容的格式，使图片格式兼容
    wa_input_cv.create_image(0, 0, anchor='nw', image=image)    # 在canvas中显示图像
    wa_input_cv.image = image   # 保留对图像对象的引用，使图像持续显示


window = tk.Tk()
window.title('深度估计')

# 菜单栏 menu bar
mb = tk.Menu(window)
window.config(menu=mb)

mb_file = tk.Menu(mb)                       # 文件菜单
mb_file.add_command(label='打开')             # 打开图片
mb_file.add_command(label='保存')             # 保存图片
mb.add_cascade(label='文件', menu=mb_file)

mb_help = tk.Menu(mb)                       # 帮助菜单
mb_help.add_command(label='说明')
mb.add_cascade(label='帮助', menu=mb_help)

# 工具栏 tool bar
tb = tk.Frame(window)
tb.pack(anchor='w')

tb_depth = tk.LabelFrame(tb, text='深度估计', labelanchor='s')   # 深度估计方法框架
tb_depth.pack(side='left', fill='y')

para_dict = {"FCRN": 'NYU_FCRN.ckpt', "MiDaS": 'model.pt', "MegaDepth": 'best_generalization_net_G.pth'}
para_key = list(para_dict.keys())      # 构造算法对权重列表的映射

tb_depth_cbb1_v = tk.StringVar()
tb_depth_lb1 = tk.Label(tb_depth, text='算法')                       # 算法
tb_depth_lb1.grid(row=1, column=1)
tb_depth_cbb1 = ttk.Combobox(tb_depth, state='readonly', textvariable=tb_depth_cbb1_v)
tb_depth_cbb1['values'] = para_key
tb_depth_cbb1.grid(row=1, column=2)
tb_depth_cbb1.current(0)

tb_depth_cbb2_v = tk.StringVar()
tb_depth_lb2 = tk.Label(tb_depth, text='权重')                      # 权重
tb_depth_lb2.grid(row=2, column=1)
tb_depth_cbb2 = ttk.Combobox(tb_depth, state='readonly', textvariable=tb_depth_cbb2_v)
tb_depth_cbb2['values'] = para_dict[tb_depth_cbb1_v.get()]
tb_depth_cbb2.grid(row=2, column=2)
tb_depth_cbb2.current(0)

tb_depth_bt = tk.Button(tb_depth, text='生成')
tb_depth_bt.grid(row=1, column=3, rowspan=2)

tb_dist = tk.LabelFrame(tb, text='距离测量', labelanchor='s')     # 距离测量框架
tb_dist.pack(side='left', fill='y')
tb_dist_lb1 = tk.Label(tb_dist, text='焦距')                      # 焦距
tb_dist_lb1.grid(row=1, column=1)
tb_dist_etr = tk.Entry(tb_dist)
tb_dist_etr.grid(row=1, column=2)
tb_dist_lb2 = tk.Label(tb_dist, text='(cm)')
tb_dist_lb2.grid(row=1, column=3)
tb_dist_lb = tk.Label(tb_dist, text='比例尺')                        # 比例尺
tb_dist_lb.grid(row=2, column=1)
tb_dist_etr = tk.Entry(tb_dist)
tb_dist_etr.grid(row=2, column=2)

tb_visual = tk.LabelFrame(tb, text='可视化效果', labelanchor='s')    # 可视化效果
tb_visual.pack(side='left', fill='y')
tb_visual_lb = tk.Label(tb_visual, text='颜色')                       # 颜色
tb_visual_lb.grid(row=1, column=1)
tb_visual_cbb = ttk.Combobox(tb_visual)
tb_visual_cbb.grid(row=1, column=2)

# 工作区域（主界面） working area
wa = tk.Frame(window)
wa.pack()

width = 600
height = 450

wa_input_cv = tk.Canvas(wa, width=width, height=height, bg='white')      # 原图帆布
wa_input_cv.create_text(width/2, height/2, text='拖拽图片到此处', fill='grey', anchor='center')
wa_input_cv.pack(side='left')
windnd.hook_dropfiles(wa_input_cv, func=show_input)                     # 将拖拽图片与wa_input_cv组件挂钩

wa_output_cv = tk.Canvas(wa, width=width, height=height, bg='white')     # 深度图帆布
wa_output_cv.pack(side='right')

# 状态栏 status bar
sb = tk.Frame(window)
sb.pack(anchor='e')

sb_message_lb1 = tk.Label(sb, text='A点：')       # A点信息
sb_message_lb1.pack(side='left')
sb_message_lb11 = tk.Label(sb, text='坐标：')
sb_message_lb11.pack(side='left')
sb_message_lb12 = tk.Label(sb, text='深度：')
sb_message_lb12.pack(side='left')

sb_message_lb01 = tk.Label(sb, text='  ')        # 间隔
sb_message_lb01.pack(side='left')

sb_message_lb2 = tk.Label(sb, text='B点：')       # B点信息
sb_message_lb2.pack(side='left')
sb_message_lb21 = tk.Label(sb, text='坐标：')
sb_message_lb21.pack(side='left')
sb_message_lb22 = tk.Label(sb, text='深度：')
sb_message_lb22.pack(side='left')

sb_message_lb02 = tk.Label(sb, text='  ')       # 间隔
sb_message_lb02.pack(side='left')

sb_message_lb3 = tk.Label(sb, text='距离：')       # 距离
sb_message_lb3.pack(side='left')


# 选择算法后选择算法的对应的权重
def mFunc(event):                                   # 触发事件
    tb_depth_cbb2_v_list = para_dict[tb_depth_cbb1_v.get()]
    tb_depth_cbb2['values'] = tb_depth_cbb2_v_list


tb_depth_cbb1.bind("<<ComboboxSelected>>", mFunc)   # 绑定事件

window.mainloop()


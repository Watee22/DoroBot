import mss
import numpy as np
import cv2

class Screen:
    def __init__(self, monitor_number=1):
        """
        初始化截图器。
        :param monitor_number: 要截取的显示器编号 (1 通常是主显示器)
        """
        try:
            # 初始化 mss，并立即获取显示器信息
            # 我们将 mss 实例保存在类中，以便将来可能重用
            self.sct = mss.mss()
            self.monitor = self.sct.monitors[monitor_number]
            print(f"[Screen] 已初始化，将截取显示器 {monitor_number}: {self.monitor}")
        except Exception as e:
            print(f"[Screen] 严重错误: 无法初始化 mss 或找到显示器 {monitor_number}。")
            print("错误详情:", e)
            print("可用的显示器:", self.sct.monitors if hasattr(self, 'sct') else "mss 未能加载")
            # 在这种严重错误下，我们应该退出
            raise

    def capture(self):
        """
        截取初始化时指定的显示器，并返回 OpenCV (BGR) 格式的图像。
        """
        # .grab() 是一个非常快的操作
        sct_img = self.sct.grab(self.monitor)
        
        # 将 BGRA 转换为 Numpy 数组
        img = np.array(sct_img)
        
        # 将 BGRA 转换为 BGR (OpenCV的标准格式)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

# --- 测试代码 ---
if __name__ == '__main__':
    import time
    print("正在测试 Screen 类...")
    screen = Screen()
    time.sleep(1) # 暂停一下，让你看到初始化信息
    
    img = screen.capture()
    print(f"截图成功，尺寸: {img.shape}")
    
    cv2.imshow('Screen Test', cv2.resize(img, (960, 540)))
    print("按任意键退出测试...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
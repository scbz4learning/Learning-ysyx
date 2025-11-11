from PIL import Image, ImageSequence
import os

# ==============================
# 配置
# ==============================
PAUSE_MS = 3000  # 结尾停顿时长（毫秒）
OVERWRITE = True  # 是否直接覆盖原文件（True 覆盖，False 新文件）
# ==============================

def process_gif(path):
    try:
        im = Image.open(path)
        loop = im.info.get("loop", 1)  # 如果没有 loop 信息，默认认为只播一次

        if loop == 0:
            print(f"⏭️  跳过 (已循环): {path}")
            return

        print(f"🔄 转换中: {path}")

        frames = []
        durations = []

        for frame in ImageSequence.Iterator(im):
            frames.append(frame.copy())
            durations.append(frame.info.get("duration", 100))  # 默认100ms

        # 在最后一帧添加停顿
        durations[-1] += PAUSE_MS

        # 生成输出文件名
        base, ext = os.path.splitext(path)
        output = base + "_loop" + ext if not OVERWRITE else path

        # 保存新 GIF
        frames[0].save(
            output,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,  # 无限循环
            disposal=2,
        )

        print(f"✅ 已保存: {output}")

    except Exception as e:
        print(f"❌ 处理失败: {path} ({e})")


def walk_and_process(root="."):
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith(".gif"):
                full_path = os.path.join(dirpath, name)
                process_gif(full_path)


if __name__ == "__main__":
    print("🚀 开始扫描 GIF 文件 ...")
    walk_and_process("docs/assets/images")
    print("🎉 全部处理完成。")

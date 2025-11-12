from PIL import Image, ImageSequence
from moviepy import VideoFileClip
import os

# ==============================
# 配置
# ==============================
PAUSE_MS = 3000      # 结尾停顿时长（毫秒）
OVERWRITE = True      # 是否覆盖原文件
MAX_FPS = 12          # 最大帧率
MAX_WIDTH = 640       # 最大宽度
MAX_HEIGHT = 480      # 最大高度
# ==============================


def resize_keep_ratio(w, h, max_w=MAX_WIDTH, max_h=MAX_HEIGHT):
    """保持比例缩放，确保宽高都不超过限制"""
    if w <= max_w and h <= max_h:
        return w, h, 1.0
    scale = min(max_w / w, max_h / h)
    return int(w * scale), int(h * scale), scale


def process_gif(path):
    """处理 GIF：停顿 + 循环 + 限帧 + 按比例压缩"""
    try:
        im = Image.open(path)
        loop = im.info.get("loop", 1)
        w, h = im.size

        # ✅ 跳过条件：已循环且分辨率不超过 640x480
        if loop == 0 and w <= MAX_WIDTH and h <= MAX_HEIGHT:
            print(f"⏭️  跳过(已循环且分辨率≤640x480): {path}")
            return

        print(f"🔄  转换 GIF: {path}")

        frames, durations = [], []
        for frame in ImageSequence.Iterator(im):
            frames.append(frame.copy())
            durations.append(frame.info.get("duration", 100))

        # 限制帧率
        fps = 1000 / (sum(durations) / len(durations)) if durations else 10
        if fps > MAX_FPS:
            scale_fps = fps / MAX_FPS
            durations = [int(d * scale_fps) for d in durations]

        # 结尾停顿
        durations[-1] += PAUSE_MS

        # 按比例调整分辨率
        new_w, new_h, scale = resize_keep_ratio(w, h)
        if scale < 1.0:
            frames = [f.resize((new_w, new_h), Image.Resampling.LANCZOS) for f in frames]
            print(f"📏 缩放比例: {scale:.3f} ({w}x{h} → {new_w}x{new_h})")

        base, ext = os.path.splitext(path)
        output = base + "_loop" + ext if not OVERWRITE else path

        frames[0].save(
            output,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,  # 无限循环
            disposal=2,
        )

        print(f"✅  已保存: {output}")

    except Exception as e:
        print(f"❌  处理失败: {path} ({e})")


def process_mp4(path):
    """将 MP4 转换为循环 GIF（保持比例，限制最大宽高和帧率）"""
    try:
        print(f"🎞️  转换 MP4 → GIF: {path}")
        clip = VideoFileClip(path)

        w, h = clip.size
        new_w, new_h, scale = resize_keep_ratio(w, h)
        if scale < 1.0:
            clip = clip.resized(scale)
            print(f"📏 缩放比例: {scale:.3f} ({w}x{h} → {new_w}x{new_h})")
        else:
            print(f"👌 尺寸合规: {w}x{h}")

        gif_path = path.rsplit(".", 1)[0] + ".gif"
        clip.write_gif(gif_path, fps=MAX_FPS)
        clip.close()

        # 再次打开GIF，加上循环和停顿
        with Image.open(gif_path) as im:
            frames, durations = [], []
            for frame in ImageSequence.Iterator(im):
                frames.append(frame.copy())
                durations.append(frame.info.get("duration", 100))
            durations[-1] += PAUSE_MS
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,
                disposal=2,
            )

        os.remove(path)
        print(f"✅  已生成循环GIF并删除视频: {gif_path}")

    except Exception as e:
        print(f"❌  转换失败: {path} ({e})")


def walk_and_process(root="."):
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            lower = name.lower()
            full_path = os.path.join(dirpath, name)
            if lower.endswith(".gif"):
                process_gif(full_path)
            elif lower.endswith(".mp4"):
                process_mp4(full_path)


if __name__ == "__main__":
    print("🚀 开始扫描 GIF / MP4 文件 ...")
    walk_and_process("docs/assets/images")
    print("🎉 全部处理完成。")

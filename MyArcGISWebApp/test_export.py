import arcpy
import os

project_path = r"D:\arcgispro\example\shiyan\shiyan.aprx" # 你的工程路径
layout_name = "布局"  # 你的布局名称
output_jpg_path = r"D:\arcgispro\MyArcGISWebApp\test_export_output.jpg" # 指定一个明确的输出路径

print(f"ArcPy 版本: {arcpy.GetInstallInfo()['Version']}")
print(f"尝试打开工程: {project_path}")

try:
    aprx = arcpy.mp.ArcGISProject(project_path)
    print(f"工程已打开。尝试查找布局: {layout_name}")

    layouts = aprx.listLayouts(layout_name)
    if layouts:
        the_layout = layouts[0]
        print(f"找到布局: {the_layout.name}")

        # 关键测试点：尝试不同的参数组合
        # 我们先严格按照 help() 输出的参数来尝试
        try:
            print(f"尝试使用 help() 输出的参数 jpeg_quality=90 导出到: {output_jpg_path}")
            the_layout.exportToJPEG(output_jpg_path, resolution=300, jpeg_quality=90)
            print(f"使用 jpeg_quality=90 导出成功！文件已保存到 {output_jpg_path}")
        except TypeError as te_jpeg_quality:
            print(f"错误 (使用 jpeg_quality=90): {te_jpeg_quality}")
            print("--- 将尝试使用 image_quality=1 ---")
            try:
                # 根据另一个错误提示尝试 image_quality
                output_jpg_path_iq = r"D:\arcgispro\MyArcGISWebApp\test_export_output_iq.jpg"
                print(f"尝试使用参数 image_quality=1 导出到: {output_jpg_path_iq}")
                the_layout.exportToJPEG(output_jpg_path_iq, resolution=300, image_quality=1)
                print(f"使用 image_quality=1 导出成功！文件已保存到 {output_jpg_path_iq}")
            except TypeError as te_image_quality:
                print(f"错误 (使用 image_quality=1): {te_image_quality}")
                print("--- 两种参数尝试均失败 ---")
                print("\n请查看 layout.exportToJPEG 的 help 文档:")
                help(the_layout.exportToJPEG) # 再次打印帮助文档确认
            except Exception as e_iq:
                print(f"使用 image_quality=1 导出时发生其他错误: {e_iq}")
        except Exception as e_general:
            print(f"使用 jpeg_quality=90 导出时发生其他错误: {e_general}")

    else:
        print(f"错误：在工程中找不到名为 '{layout_name}' 的布局。")
        all_layouts = [lyt.name for lyt in aprx.listLayouts()]
        print(f"工程中可用的布局有: {', '.join(all_layouts) if all_layouts else '无'}")

except RuntimeError as rt_err:
    print(f"打开工程或操作时发生运行时错误: {rt_err}")
except Exception as e:
    print(f"发生未知错误: {e}")
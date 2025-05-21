import arcpy
import os
import json
import sys #  确保导入 sys 以便在测试块中使用 sys.exit()

# --- 配置默认输出工作空间 ---
# 使用你之前确认的路径
EXPORT_OUTPUT_WORKSPACE = r"D:\arcgispro\MyArcGISWeb\MyArcGISWebApp\OutputData"

def export_map_layout(aprx_path, layout_name, output_name_no_ext, output_format="PDF", resolution_dpi=300):
    """
    导出指定 ArcGIS Pro 工程中的布局。
    (函数内部代码与我之前提供的“完整代码 - 包含详细错误捕获和日志”的版本一致)
    """
    try:
        print(f"[export_map_tool.py] Script started. APRX: {aprx_path}, Layout: {layout_name}")
        arcpy.env.overwriteOutput = True

        if not os.path.exists(EXPORT_OUTPUT_WORKSPACE):
            try:
                os.makedirs(EXPORT_OUTPUT_WORKSPACE)
                print(f"[export_map_tool.py] Created output workspace: {EXPORT_OUTPUT_WORKSPACE}")
            except Exception as e_mkdir:
                errmsg_mkdir = f"创建输出目录 '{EXPORT_OUTPUT_WORKSPACE}' 失败: {str(e_mkdir)}"
                print(f"[export_map_tool.py] Error: {errmsg_mkdir}")
                return {"status": "error", "message": errmsg_mkdir}

        file_extension = output_format.lower()
        if file_extension == "jpeg":
            file_extension = "jpg"

        safe_output_name = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in output_name_no_ext.strip())
        if not safe_output_name:
            safe_output_name = "exported_map_default_name" # 提供一个更有意义的默认名

        output_file_full_path = os.path.join(EXPORT_OUTPUT_WORKSPACE, f"{safe_output_name}.{file_extension}")

        print(f"[export_map_tool.py] Target output file: {output_file_full_path}")
        print(f"[export_map_tool.py] Exporting with Format: {output_format}, DPI: {resolution_dpi if resolution_dpi else 'Default'}")

        if not os.path.exists(aprx_path) or not aprx_path.lower().endswith(".aprx"):
            errmsg = f"指定的工程文件无效或在服务器上未找到: {aprx_path}"
            print(f"[export_map_tool.py] Error: {errmsg}")
            return {"status": "error", "message": errmsg}

        aprx = None
        try:
            aprx = arcpy.mp.ArcGISProject(aprx_path)
            layout_to_export_list = aprx.listLayouts(layout_name)

            if not layout_to_export_list:
                available_layouts = [l.name for l in aprx.listLayouts()]
                errmsg = f"在工程 '{os.path.basename(aprx_path)}' 中未找到名为 '{layout_name}' 的布局。可用布局: {available_layouts}"
                print(f"[export_map_tool.py] Error: {errmsg}")
                return {"status": "error", "message": errmsg}

            lyt = layout_to_export_list[0]
            print(f"[export_map_tool.py] Layout '{lyt.name}' found.")

            actual_dpi = resolution_dpi if resolution_dpi and resolution_dpi > 0 else 300 # 确保DPI有效

            if output_format.upper() == "PDF":
                lyt.exportToPDF(output_file_full_path, resolution=actual_dpi)
            elif output_format.upper() == "PNG":
                lyt.exportToPNG(output_file_full_path, resolution=actual_dpi)
            elif output_format.upper() == "JPEG":
                lyt.exportToJPEG(output_file_full_path, resolution=actual_dpi)
            elif output_format.upper() == "SVG":
                lyt.exportToSVG(output_file_full_path, convert_text_to_path=False)
            elif output_format.upper() == "TIFF":
                lyt.exportToTIFF(output_file_full_path, resolution=actual_dpi)
            else:
                errmsg = f"不支持的输出格式: {output_format}. 支持的格式包括 PDF, PNG, JPEG, SVG, TIFF."
                print(f"[export_map_tool.py] Error: {errmsg}")
                return {"status": "error", "message": errmsg}
        finally:
            if aprx:
                del aprx
                print("[export_map_tool.py] ArcGISProject object released.")

        if os.path.exists(output_file_full_path) and os.path.getsize(output_file_full_path) > 0:
            success_message = f"地图布局 '{layout_name}' 已成功导出为 {output_format} 格式。"
            print(f"[export_map_tool.py] Success: {success_message} Path: {output_file_full_path}")
            return {"status": "success", "message": success_message, "output_path": output_file_full_path}
        else:
            errmsg = f"地图导出操作已执行，但输出文件 '{output_file_full_path}' 未创建或为空。"
            print(f"[export_map_tool.py] Error: {errmsg}")
            return {"status": "error", "message": errmsg}

    except arcpy.ExecuteError:
        error_messages = arcpy.GetMessages(2)
        print(f"[export_map_tool.py] arcpy.ExecuteError: {error_messages}")
        return {"status": "error", "message": f"ArcGIS 处理错误: {error_messages}"}
    except RuntimeError as rt_err:
        error_str = str(rt_err)
        print(f"[export_map_tool.py] RuntimeError: {error_str}")
        return {"status": "error", "message": f"ArcGIS 运行时错误: {error_str}"}
    except Exception as e:
        error_str = str(e)
        print(f"[export_map_tool.py] Python Exception: {error_str}")
        return {"status": "error", "message": f"执行导出脚本时发生意外的服务器内部错误: {error_str}"}

# 这部分用于你直接在命令行或 IDE 中测试这个脚本文件
if __name__ == '__main__':
    print("--- Testing export_map_tool.py script ---")

    # --- ↓↓↓ 请务必替换为你本地有效的测试路径和参数 ↓↓↓ ---
    # 1. 确保这个 APRX 文件真实存在于你的服务器/电脑上
    # 2. 确保该 APRX 文件中有一个名为你指定的 test_layout_name 的布局
    # 3. 确保 EXPORT_OUTPUT_WORKSPACE 路径 (脚本顶部定义) 存在且你有写入权限

    test_aprx_file = r"D:\arcgispro\example\shiyan\shiyan.aprx"  # <<--- !!! 修改为你 APRX 文件的真实路径 !!!
    test_layout_name = "布局"  # <<--- !!! 修改为你 APRX 文件中一个真实存在的布局名称 !!!
    test_output_filename_no_ext = "MyMapFromScriptTest_Feng"
    test_output_format = "PNG" # 可选 "PDF", "PNG", "JPEG", "SVG", "TIFF"
    test_resolution = 150     # DPI 值

    # 检查输出目录是否存在，如果不存在则创建 (脚本内部也会检查，但这里多一层保障)
    if not os.path.exists(EXPORT_OUTPUT_WORKSPACE):
        try:
            os.makedirs(EXPORT_OUTPUT_WORKSPACE)
            print(f"Created EXPORT_OUTPUT_WORKSPACE for test: {EXPORT_OUTPUT_WORKSPACE}")
        except Exception as e:
            print(f"ERROR: Could not create EXPORT_OUTPUT_WORKSPACE '{EXPORT_OUTPUT_WORKSPACE}'. Error: {e}")
            sys.exit(1) # 如果无法创建输出目录，测试无法进行

    if not os.path.exists(test_aprx_file):
        print(f"ERROR: Test APRX file not found at '{test_aprx_file}'. Please set a valid path for 'test_aprx_file'.")
    else:
        print(f"\nTest Parameters:")
        print(f"  APRX Path: {test_aprx_file}")
        print(f"  Layout Name: {test_layout_name}")
        print(f"  Output Filename (no ext): {test_output_filename_no_ext}")
        print(f"  Output Format: {test_output_format}")
        print(f"  Resolution (DPI): {test_resolution}")
        print(f"  Output Workspace (defined in script): {EXPORT_OUTPUT_WORKSPACE}")
        print("-" * 30)

        result = export_map_layout(
            test_aprx_file,
            test_layout_name,
            test_output_filename_no_ext,
            test_output_format,
            test_resolution
        )

        print("\n--- Script Execution Result ---")
        # ensure_ascii=False 保证中文字符在打印时能正确显示
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("status") == "success":
            print(f"\nSUCCESS! Output file should be at: {result.get('output_path')}")
        else:
            print(f"\nERROR! Message: {result.get('message')}")

    print("\n--- Test script finished ---")
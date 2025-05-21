import arcpy
import json
import os # 用于处理路径和创建文件夹

# --- 配置输出工作空间 (非常重要！) ---
# 修改为你服务器上实际的、ArcGIS Pro 有写入权限的路径
# ArcPy 脚本将在这里创建输出的 shapefile 或要素类
# 确保这个文件夹存在，或者脚本有权限创建它
OUTPUT_WORKSPACE = r"D:\arcgispro\MyArcGISWebApp\OutputData" # 示例路径，请务必修改！

# --- （可选）配置输入数据的基础路径 ---
# 如果前端只传递文件名，你可能需要一个基础路径来拼接
# INPUT_DATA_BASE_PATH = r"D:\arcgispro\MyArcGISWebApp\InputData" # 示例路径

def perform_buffer_analysis(input_fc_path, output_name, distance_with_units, dissolve_type="NONE"):
    """
    执行缓冲区分析并返回结果。
    参数:
        input_fc_path (str): 输入要素类的完整路径 (或相对于某个已知工作空间的路径)。
        output_name (str): 输出要素类的名称 (不含路径和后缀)。
        distance_with_units (str): 缓冲区距离和单位 (例如 "100 Meters")。
        dissolve_type (str): 融合选项 ("NONE", "ALL", "LIST")。
    返回:
        dict: 包含 'status' 和 'message' (以及可能的 'output_path') 的字典。
    """
    try:
        arcpy.env.overwriteOutput = True # 允许覆盖已存在的输出

        # 确保输出工作空间存在
        if not os.path.exists(OUTPUT_WORKSPACE):
            os.makedirs(OUTPUT_WORKSPACE)
            print(f"Created output workspace: {OUTPUT_WORKSPACE}")

        # 构建完整的输出路径 (假设输出为 Shapefile)
        # 你可以根据需要修改为输出到文件地理数据库 (.gdb)
        output_fc_full_path = os.path.join(OUTPUT_WORKSPACE, f"{output_name}.shp")

        print(f"ArcPy - Executing Buffer:")
        print(f"  Input Feature Class: {input_fc_path}")
        print(f"  Output Feature Class: {output_fc_full_path}")
        print(f"  Buffer Distance: {distance_with_units}")
        print(f"  Dissolve Option: {dissolve_type}")

        # 执行缓冲区分析
        arcpy.analysis.Buffer(
            in_features=input_fc_path,
            out_feature_class=output_fc_full_path,
            buffer_distance_or_field=distance_with_units,
            dissolve_option=dissolve_type
            # 你可以根据需要添加其他参数，如 sideType, endType
        )

        if arcpy.Exists(output_fc_full_path):
            success_message = f"缓冲区分析成功完成。结果已保存到: {output_fc_full_path}"
            print(success_message)
            return {"status": "success", "message": success_message, "output_path": output_fc_full_path}
        else:
            error_message_arcpy = "ArcPy 错误：缓冲区结果未生成或找不到。"
            print(error_message_arcpy)
            return {"status": "error", "message": error_message_arcpy}

    except arcpy.ExecuteError:
        error_messages = arcpy.GetMessages(2) # 获取 ArcGIS 错误信息
        print(f"ArcPy ExecuteError: {error_messages}")
        return {"status": "error", "message": f"ArcGIS 处理错误: {error_messages}"}
    except Exception as e:
        error_str = str(e)
        print(f"Python Exception in perform_buffer_analysis: {error_str}")
        return {"status": "error", "message": f"执行脚本时发生服务器内部错误: {error_str}"}

if __name__ == '__main__':
    # 这部分用于你直接在命令行或 IDE 中测试这个脚本文件
    print("Testing buffer_tool.py script...")
    # --- 请替换为你本地有效的测试路径和参数 ---
    # 确保这些路径和文件存在，并且你有写入 OUTPUT_WORKSPACE 的权限
    # 例如:
    # test_input = r"C:\GIS_Data\Inputs\test_points.shp"
    # test_output_name = "my_test_buffer"
    # test_distance = "250 Meters"
    # test_dissolve = "NONE"
    #
    # print(f"Test parameters: Input='{test_input}', Output Name='{test_output_name}', Distance='{test_distance}', Dissolve='{test_dissolve}'")
    # result = perform_buffer_analysis(test_input, test_output_name, test_distance, test_dissolve)
    # print("\nScript execution result:")
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    print("To test, uncomment the example lines above and provide valid paths.")
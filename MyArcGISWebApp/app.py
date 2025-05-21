import sys
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- 动态添加脚本路径，以便可以导入自定义工具模块 ---
current_file_dir = os.path.dirname(os.path.abspath(__file__))
scripts_folder_path = os.path.join(current_file_dir, 'scripts')
if scripts_folder_path not in sys.path:
    sys.path.insert(0, scripts_folder_path)
    print(f"Appended to sys.path: {scripts_folder_path}")

# --- 尝试导入 ArcPy 工具函数 ---
# 缓冲区分析工具
try:
    from buffer_tool import perform_buffer_analysis

    print(f"Successfully imported 'perform_buffer_analysis' from buffer_tool.py.")
except ImportError as e:
    print(f"ImportError: Could not import 'perform_buffer_analysis' from buffer_tool.py. Error: {e}")


    def perform_buffer_analysis(*args, **kwargs):  # 占位函数
        return {"status": "error", "message": "GIS脚本 (buffer_tool.py) 未找到或导入失败。"}
except Exception as e_imp_buffer:
    print(f"Unexpected error importing buffer_tool: {e_imp_buffer}")


    def perform_buffer_analysis(*args, **kwargs):
        return {"status": "error", "message": f"导入buffer_tool时发生意外错误: {e_imp_buffer}"}

# 导出地图工具
try:
    from export_map_tool import export_map_layout

    print(f"Successfully imported 'export_map_layout' from export_map_tool.py.")
except ImportError as e:
    print(f"ImportError: Could not import 'export_map_layout' from export_map_tool.py. Error: {e}")


    def export_map_layout(*args, **kwargs):  # 占位函数
        return {"status": "error", "message": "GIS脚本 (export_map_tool.py) 未找到或导入失败。"}
except Exception as e_imp_export:
    print(f"Unexpected error importing export_map_tool: {e_imp_export}")


    def export_map_layout(*args, **kwargs):
        return {"status": "error", "message": f"导入export_map_tool时发生意外错误: {e_imp_export}"}

# --- 初始化 Flask 应用 ---
app = Flask(__name__)

# --- CORS 配置 ---
# 允许来自 Vue 开发服务器 (例如 http://localhost:8080 或 http://localhost:8081) 的跨域请求
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080", "http://localhost:8081"]}})


# --- API 端点定义 ---

@app.route('/')
def hello():
    print("[Flask API] Root path '/' accessed.")
    return "Feng's WebGIS Backend is up and running!"


@app.route('/api/gis/buffer_analysis', methods=['POST'])
def api_buffer_analysis():
    print("\n[Flask API] Received POST request for /api/gis/buffer_analysis")
    try:
        data = request.get_json()
        if not data:
            print("[Flask API] Error: No input JSON data provided.")
            return jsonify({"status": "error", "message": "请求体中未提供JSON数据。"}), 400

        print(f"[Flask API] Received data for buffer: {json.dumps(data, indent=2)}")

        aprx_file_path = data.get('aprxPath')
        input_layer_name_in_toc = data.get('inputLayerValue')  # 来自 BufferAnalysisForm 的 v-model
        output_layer_name_no_ext = data.get('outputLayerName')
        buffer_distance_val = data.get('bufferDistance')
        distance_units_val = data.get('distanceUnits')
        dissolve_type_val = data.get('dissolveType', 'NONE')

        if not all([aprx_file_path, input_layer_name_in_toc, output_layer_name_no_ext,
                    buffer_distance_val is not None, distance_units_val]):
            return jsonify({"status": "error", "message": "缓冲区分析缺少必要参数。"}), 400

        actual_input_fc_path_on_server = None
        try:
            arcpy = __import__('arcpy')  # 动态导入，确保只在需要时尝试
            if not os.path.exists(aprx_file_path) or not aprx_file_path.lower().endswith(".aprx"):
                return jsonify(
                    {"status": "error", "message": f"指定的工程文件无效或在服务器上未找到: {aprx_file_path}"}), 404

            aprx = arcpy.mp.ArcGISProject(aprx_file_path)
            map_list = aprx.listMaps()
            if not map_list:
                return jsonify(
                    {"status": "error", "message": f"工程 '{os.path.basename(aprx_file_path)}' 中没有地图。"}), 404

            active_map = map_list[0]  # 假设操作第一个地图
            found_layers = active_map.listLayers(input_layer_name_in_toc)

            if found_layers:
                input_layer_object = found_layers[0]
                if input_layer_object.supports("dataSource"):
                    actual_input_fc_path_on_server = input_layer_object.dataSource
                    if not actual_input_fc_path_on_server or not arcpy.Exists(actual_input_fc_path_on_server):
                        return jsonify({"status": "error",
                                        "message": f"图层 '{input_layer_name_in_toc}' 的数据源 '{actual_input_fc_path_on_server}' 无效或未找到。"}), 404
                else:
                    return jsonify({"status": "error",
                                    "message": f"图层 '{input_layer_name_in_toc}' 不支持 dataSource 属性。"}), 400
            else:
                return jsonify({"status": "error",
                                "message": f"在地图 '{active_map.name}' 中未找到图层 '{input_layer_name_in_toc}'。"}), 404
        except Exception as e_path:
            return jsonify({"status": "error", "message": f"处理工程或图层路径时出错: {str(e_path)}"}), 500

        buffer_distance_str_for_arcpy = f"{buffer_distance_val} {distance_units_val}"

        print(
            f"[Flask API] Calling perform_buffer_analysis with: Input='{actual_input_fc_path_on_server}', OutputName='{output_layer_name_no_ext}', Distance='{buffer_distance_str_for_arcpy}', Dissolve='{dissolve_type_val}'")
        result_from_script = perform_buffer_analysis(
            actual_input_fc_path_on_server,
            output_layer_name_no_ext,
            buffer_distance_str_for_arcpy,
            dissolve_type_val
        )
        return jsonify(result_from_script)

    except Exception as e_main:
        print(f"[Flask API] Major exception in api_buffer_analysis: {str(e_main)}")
        return jsonify(
            {"status": "error", "message": f"服务器处理缓冲区分析请求时发生严重内部错误: {str(e_main)}"}), 500


@app.route('/api/gis/export_map', methods=['POST'])
def api_export_map():
    print("\n[Flask API] Received POST request for /api/gis/export_map")
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "请求体中未提供JSON数据。"}), 400

        print(f"[Flask API] Received data for map export: {json.dumps(data, indent=2)}")

        aprx_file_path = data.get('aprxPath')
        layout_name_from_form = data.get('layoutName')
        output_format_from_form = data.get('outputFormat', 'PDF')
        output_name_from_form = data.get('outputName')
        resolution_dpi_from_form = data.get('dpi', 300)

        if not all([aprx_file_path, layout_name_from_form, output_name_from_form]):
            return jsonify({"status": "error", "message": "导出地图缺少必要参数：工程路径、布局名称或输出文件名称。"}), 400

        if resolution_dpi_from_form is not None and (
                not isinstance(resolution_dpi_from_form, int) or resolution_dpi_from_form <= 0):
            resolution_dpi_from_form = 300  # 如果 DPI 无效，使用默认值

        print(
            f"[Flask API] Parameters for map export: APRX='{aprx_file_path}', Layout='{layout_name_from_form}', Format='{output_format_from_form}', OutputName='{output_name_from_form}', DPI='{resolution_dpi_from_form}'")

        result_from_script = export_map_layout(
            aprx_path=aprx_file_path,
            layout_name=layout_name_from_form,
            output_name_no_ext=output_name_from_form,
            output_format=output_format_from_form,
            resolution_dpi=resolution_dpi_from_form
        )
        print(f"[Flask API] ArcPy export script result: {json.dumps(result_from_script, indent=2, ensure_ascii=False)}")
        return jsonify(result_from_script)

    except Exception as e_main:
        error_str = str(e_main)
        print(f"[Flask API] Major exception in api_export_map: {error_str}")
        return jsonify({"status": "error", "message": f"服务器处理导出地图请求时发生严重内部错误: {str(e_main)}"}), 500
@app.route('/simple_test_path', methods=['GET'])
def simple_test():
    print("[Flask API] /simple_test_path accessed via GET")
    return jsonify({"message": "Simple test path on Flask is working!"})

if __name__ == '__main__':
    print("Starting Feng's WebGIS Flask development server...")
    # 确保 Flask 服务器运行在能够访问 ArcPy 的 Python 环境中 (例如 arcgis-flask-env)
    app.run(host='0.0.0.0', port=5000, debug=True)  # debug=True 方便开发，生产环境应设为False
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pathlib import Path
import zipfile
import os
import subprocess
import tempfile

try:
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

class VisualGraphGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        if not HAS_MATPLOTLIB:
            print("⚠️ matplotlib not available. Install with: pip install matplotlib networkx")

    def create_project_structure_graph(self, project_analysis: Dict, project_name: str) -> str:
        if not HAS_MATPLOTLIB:
            return "matplotlib not available"

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        fig.suptitle(f'{project_name} - Project Structure', fontsize=16, fontweight='bold')

        files_by_lang = {}
        for file_info in project_analysis.get('files', []):
            lang = file_info.get('analysis', {}).get('language', 'Unknown')
            files_by_lang.setdefault(lang, []).append(file_info)

        colors = plt.cm.Set3(np.linspace(0, 1, len(files_by_lang)))
        y_pos = 9

        for i, (lang, files) in enumerate(files_by_lang.items()):
            lang_box = patches.FancyBboxPatch((0.5, y_pos - 0.3), 2, 0.6, boxstyle="round,pad=0.1",
                                             facecolor=colors[i], edgecolor='black')
            ax.add_patch(lang_box)
            ax.text(1.5, y_pos, lang, ha='center', va='center', fontsize=12, fontweight='bold')

            x_pos = 3.5
            for file_info in files[:6]:
                file_path = file_info.get('path', 'unknown')
                file_name = Path(file_path).name
                if len(file_name) > 12:
                    file_name = file_name[:9] + "..."

                file_box = patches.FancyBboxPatch((x_pos, y_pos - 0.25), 1.2, 0.5, boxstyle="round,pad=0.05",
                                                 facecolor='lightblue', edgecolor='navy')
                ax.add_patch(file_box)
                ax.text(x_pos + 0.6, y_pos, file_name, ha='center', va='center', fontsize=8)

                x_pos += 1.4
                if x_pos > 8.5:
                    break
            y_pos -= 1.2
            if y_pos < 1:
                break

        output_path = self.output_dir / f'{project_name}_structure.png'
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)

    def create_file_dependency_graph(self, file_path: str, analysis: Dict, project_name: str) -> str:
        if not HAS_MATPLOTLIB:
            return "matplotlib not available"

        G = nx.DiGraph()
        file_name = Path(file_path).stem
        G.add_node(file_name, node_type='main', color='red')

        for imp in analysis.get('imports', [])[:10]:
            clean_imp = imp.split('.')[-1] if '.' in imp else imp
            G.add_node(clean_imp, node_type='import', color='lightblue')
            G.add_edge(clean_imp, file_name)

        for cls in analysis.get('classes', [])[:5]:
            G.add_node(cls, node_type='class', color='lightgreen')
            G.add_edge(file_name, cls)

        for func in analysis.get('functions', [])[:8]:
            if func not in analysis.get('classes', []):
                G.add_node(func, node_type='function', color='lightyellow')
                G.add_edge(file_name, func)

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=3, iterations=50)
        node_colors = {'main': 'red', 'import': 'lightblue', 'class': 'lightgreen', 'function': 'lightyellow'}

        for node_type, color in node_colors.items():
            nodes = [n for n in G.nodes() if G.nodes[n].get('node_type') == node_type]
            if nodes:
                nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=color, node_size=2000, alpha=0.8)

        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        plt.title(f'Dependency Graph: {file_name}', fontsize=14, fontweight='bold')
        plt.axis('off')

        output_path = self.output_dir / f'{project_name}_{file_name}_deps.png'
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)

    def create_complexity_heatmap(self, project_analysis: Dict, project_name: str) -> str:
        if not HAS_MATPLOTLIB:
            return "matplotlib not available"

        files = project_analysis.get('files', [])
        if not files:
            return "No files to analyze"

        file_names, complexity_scores, line_counts = [], [], []
        for file_info in files[:20]:
            path = file_info.get('path', 'unknown')
            analysis = file_info.get('analysis', {})
            file_name = Path(path).stem
            if len(file_name) > 15:
                file_name = file_name[:12] + "..."

            lines = analysis.get('lines', 0)
            classes = len(analysis.get('classes', []))
            functions = len(analysis.get('functions', []))
            complexity = (lines * 0.1) + (classes * 5) + (functions * 2)

            file_names.append(file_name)
            complexity_scores.append(complexity)
            line_counts.append(lines)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
        complexity_matrix = np.array(complexity_scores).reshape(-1, 1)
        im1 = ax1.imshow(complexity_matrix, cmap='YlOrRd', aspect='auto')
        ax1.set_yticks(range(len(file_names)))
        ax1.set_yticklabels(file_names)
        ax1.set_xticks([])
        ax1.set_title('Code Complexity Score')
        plt.colorbar(im1, ax=ax1)

        lines_matrix = np.array(line_counts).reshape(-1, 1)
        im2 = ax2.imshow(lines_matrix, cmap='Blues', aspect='auto')
        ax2.set_yticks(range(len(file_names)))
        ax2.set_yticklabels(file_names)
        ax2.set_xticks([])
        ax2.set_title('Lines of Code')
        plt.colorbar(im2, ax=ax2)

        plt.suptitle(f'{project_name} - Code Metrics', fontsize=14)
        output_path = self.output_dir / f'{project_name}_complexity.png'
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)

        def extract_plots_from_file(self, file_path: str, project_name: str) -> List[str]:
            if not HAS_MATPLOTLIB:
                return []

            if Path(file_path).suffix != '.py':
                return []

            output_paths = []
            with tempfile.TemporaryDirectory() as tmpdir:
                wrapper_script = Path(tmpdir) / 'run_plots.py'
                with open(wrapper_script, 'w') as f:
                    f.write(f"""
    import matplotlib.pyplot as plt
    import os
    plt.switch_backend('Agg')  # Non-interactive backend
    try:
        with open('{file_path}') as f:
            code = f.read()
        exec(code, {{'plt': plt}})
        for i, fig in enumerate(plt.get_fignums()):
            plt.figure(i)
            plt.savefig(os.path.join('{tmpdir}', f'plot_{{i}}.png'))
            plt.close()
    except Exception:
        pass
    """)
                try:
                    subprocess.run(['python', str(wrapper_script)], check=True, capture_output=True)
                    for i in range(100):  # Arbitrary limit
                        plot_path = Path(tmpdir) / f'plot_{i}.png'
                        if plot_path.exists():
                            dest_path = self.output_dir / f'{project_name}_plot_{i}.png'
                            os.rename(plot_path, dest_path)
                            output_paths.append(str(dest_path))
                except subprocess.CalledProcessError:
                    pass
            return output_paths

        def create_graph_zip(self, file_path: str, analysis: Dict, project_name: str) -> str:
            if not HAS_MATPLOTLIB:
                return "matplotlib not available"

            graphs = []
            dep_graph = self.create_file_dependency_graph(file_path, analysis, project_name)
            if dep_graph != "matplotlib not available":
                graphs.append(dep_graph)
            graphs.extend(self.extract_plots_from_file(file_path, project_name))

            zip_path = self.output_dir / f'{project_name}_graphs.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for graph in graphs:
                    if os.path.exists(graph):
                        zipf.write(graph, os.path.basename(graph))
            return str(zip_path)
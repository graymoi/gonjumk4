"""
城乡建设政策知识服务系统
主入口文件
"""

import sys
import json
from pathlib import Path
from datetime import datetime

from core.intent_analyzer import IntentAnalyzer
from core.workflow_engine import WorkflowEngine
from core.skill_scheduler import SkillScheduler
from core.parts_library import PartsLibrary, auto_collect_parts
from core.evolution_engine import EvolutionEngine
from auto_update import update_readme, git_commit


class PolicyKnowledgeSystem:
    """城乡建设政策知识服务系统"""
    
    def __init__(self):
        self.intent_analyzer = IntentAnalyzer()
        self.workflow_engine = WorkflowEngine()
        self.skill_scheduler = SkillScheduler()
        self.parts_library = PartsLibrary()
        self.evolution_engine = EvolutionEngine()
        
        print("=" * 60)
        print("城乡建设政策知识服务系统 v1.1.0")
        print("可生长、自动进化的AI自动化系统")
        print("=" * 60)
        print()
    
    def process(self, user_input: str) -> Dict:
        """处理用户输入"""
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 收到用户输入: {user_input}")
        print()
        
        print("Step 1: 意图分析...")
        intent_result = self.intent_analyzer.analyze(user_input)
        print(f"  意图: {intent_result['intent']}")
        print(f"  置信度: {intent_result['confidence']:.2f}")
        print(f"  关键词: {intent_result['keywords']}")
        print()
        
        print("Step 2: 场景生成...")
        scenario = self.intent_analyzer.generate_scenario(intent_result)
        print(f"  场景名称: {scenario['name']}")
        print(f"  所需技能: {scenario['required_skills']}")
        print()
        
        print("Step 3: 工作流生成...")
        workflow = self.workflow_engine.generate_workflow(intent_result, scenario)
        print(f"  工作流: {workflow['workflow_name']}")
        print(f"  步骤数: {len(workflow['steps'])}")
        print()
        
        print("Step 4: 工作流执行...")
        context = {
            "user_input": user_input,
            "intent": intent_result,
            "scenario": scenario
        }
        workflow_result = self.workflow_engine.execute_workflow(workflow, context)
        print(f"  状态: {workflow_result['status']}")
        print()
        
        print("Step 5: 零件提取...")
        parts_result = auto_collect_parts(self.parts_library, workflow_result)
        print(f"  提取零件: {parts_result['added']}个")
        print()
        
        print("Step 6: 系统进化...")
        evolution_result = self.evolution_engine.evolve_after_interaction({
            "id": datetime.now().strftime('%Y%m%d%H%M%S'),
            "user_input": user_input,
            "intent": intent_result["intent"],
            "scenario": scenario["name"],
            "skills_used": [s.get("skill") for s in workflow.get("steps", [])],
            "success": workflow_result["status"] == "completed",
            "parts_extracted": parts_result["added"]
        })
        print(f"  进化状态: 完成")
        print()
        
        print("Step 7: 结果输出...")
        output = self._generate_output(workflow_result)
        print(f"  输出目录: {output['output_dir']}")
        print()
        
        print("Step 8: 更新系统...")
        update_readme()
        print()
        
        return {
            "intent": intent_result,
            "scenario": scenario,
            "workflow": workflow_result,
            "parts": parts_result,
            "evolution": evolution_result,
            "output": output
        }
    
    def _generate_output(self, workflow_result: Dict) -> Dict:
        """生成输出"""
        
        timestamp = datetime.now().strftime('%Y-%m-%d')
        scenario_name = workflow_result.get("workflow_name", "通用工作流").replace("工作流", "")
        
        output_dir = Path(f"outputs/{timestamp}_{scenario_name}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(workflow_result, f, ensure_ascii=False, indent=2)
        
        return {
            "output_dir": str(output_dir),
            "output_file": str(output_file),
            "status": "success"
        }
    
    def interactive_mode(self):
        """交互模式"""
        
        print("进入交互模式，输入 'exit' 退出")
        print()
        
        while True:
            try:
                user_input = input("请输入您的需求: ").strip()
                
                if user_input.lower() in ['exit', 'quit', '退出']:
                    print("感谢使用，再见！")
                    break
                
                if not user_input:
                    continue
                
                result = self.process(user_input)
                
                print("-" * 60)
                print("处理完成！")
                print("-" * 60)
                print()
                
            except KeyboardInterrupt:
                print("\n感谢使用，再见！")
                break
            except Exception as e:
                print(f"错误: {e}")
                print()
    
    def command_mode(self, command: str, params: str = ""):
        """命令模式"""
        
        commands = {
            "谋划": self._cmd_project_planning,
            "筛选": self._cmd_project_filter,
            "研究": self._cmd_policy_research,
            "组装": self._cmd_quick_assemble,
            "宣讲": self._cmd_presentation,
            "统计": self._cmd_stats,
            "帮助": self._cmd_help
        }
        
        if command in commands:
            commands[command](params)
        else:
            print(f"未知命令: {command}")
            print("输入 '帮助' 查看可用命令")
    
    def _cmd_project_planning(self, params: str):
        """项目谋划命令"""
        user_input = f"谋划一个{params}项目"
        self.process(user_input)
    
    def _cmd_project_filter(self, params: str):
        """项目筛选命令"""
        user_input = f"筛选{params}项目"
        self.process(user_input)
    
    def _cmd_policy_research(self, params: str):
        """政策研究命令"""
        user_input = f"研究{params}政策"
        self.process(user_input)
    
    def _cmd_quick_assemble(self, params: str):
        """快速组装命令"""
        user_input = f"组装{params}材料"
        self.process(user_input)
    
    def _cmd_presentation(self, params: str):
        """宣讲材料命令"""
        user_input = f"组装{params}宣讲PPT"
        self.process(user_input)
    
    def _cmd_stats(self, params: str):
        """统计命令"""
        
        print("系统统计信息:")
        print()
        
        workflow_stats = self.workflow_engine.get_workflow_stats()
        print(f"工作流统计:")
        print(f"  总数: {workflow_stats['total']}")
        print(f"  成功: {workflow_stats['completed']}")
        print(f"  失败: {workflow_stats['failed']}")
        print(f"  成功率: {workflow_stats['success_rate']:.2%}")
        print()
        
        skill_stats = self.skill_scheduler.get_stats()
        print(f"技能统计:")
        print(f"  总数: {skill_stats['total_skills']}")
        print()
        
        categories = self.skill_scheduler.get_skills_by_category()
        print("技能分类:")
        for category, skills in categories.items():
            print(f"  {category}: {len(skills)}个")
        print()
        
        parts_stats = self.parts_library.get_stats()
        print(f"零件库统计:")
        print(f"  总数: {parts_stats['total']}")
        for part_type, count in parts_stats['by_type'].items():
            print(f"  {part_type}: {count}个")
        print()
        
        evolution_report = self.evolution_engine.get_evolution_report()
        print(f"系统进化:")
        print(f"  总交互: {evolution_report['metrics']['total_interactions']}")
        print(f"  成功率: {evolution_report['success_rate']}")
        print(f"  零件增长: {evolution_report['metrics']['parts_added']}个")
        print()
    
    def _cmd_help(self, params: str):
        """帮助命令"""
        
        print("可用命令:")
        print()
        print("  /谋划 <项目描述>  - 项目谋划")
        print("  /筛选 <项目列表>  - 项目筛选")
        print("  /研究 <政策关键词> - 政策研究")
        print("  /组装 <主题>      - 快速组装")
        print("  /宣讲 <主题>      - 生成宣讲PPT")
        print("  /统计            - 查看系统统计")
        print("  /帮助            - 显示帮助信息")
        print("  /exit            - 退出系统")
        print()


def main():
    """主函数"""
    
    system = PolicyKnowledgeSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        params = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        
        if command.startswith("/"):
            command = command[1:]
        
        system.command_mode(command, params)
    else:
        system.interactive_mode()


if __name__ == "__main__":
    main()

"""
城乡建设政策知识服务系统
主入口文件
"""

import sys
import json
from pathlib import Path
from datetime import datetime

from core.logger import get_system_logger
from core.output_manager import OutputManager
from core.intent_analyzer import IntentAnalyzer
from core.workflow_engine import WorkflowEngine
from core.skill_scheduler import SkillScheduler
from core.parts_library import PartsLibrary, auto_collect_parts
from core.evolution_engine import EvolutionEngine
from core.evolution_monitor import EvolutionMonitor
from core.continuous_optimizer import ContinuousOptimizer
from core.auto_loop_engine import AutoLoopEngine
from core.workflow_scheduler import WorkflowScheduler, WorkflowOrchestrator
from core.continuous_learning import ContinuousLearningEngine
from adapters.policy_adapter import PolicyAdapter
from hooks.hooks import hook_manager


class PolicyKnowledgeSystem:
    """城乡建设政策知识服务系统"""
    
    def __init__(self):
        self.logger = get_system_logger()
        self.output_manager = OutputManager()
        self.intent_analyzer = IntentAnalyzer()
        self.workflow_engine = WorkflowEngine()
        self.skill_scheduler = SkillScheduler()
        self.parts_library = PartsLibrary()
        self.evolution_engine = EvolutionEngine()
        self.evolution_monitor = EvolutionMonitor()
        self.continuous_optimizer = ContinuousOptimizer()
        self.policy_adapter = PolicyAdapter()
        
        self.auto_loop_engine = AutoLoopEngine(self)
        self.workflow_scheduler = WorkflowScheduler(self.auto_loop_engine)
        self.workflow_orchestrator = WorkflowOrchestrator(self.auto_loop_engine, self.workflow_scheduler)
        self.continuous_learning = ContinuousLearningEngine()
        
        self._print_banner()
    
    def _print_banner(self):
        """打印系统横幅"""
        print("=" * 60)
        print("城乡建设政策知识服务系统 v3.0.0")
        print("可生长、自动进化的AI自动化系统")
        print("支持自动化循环工作 (Loop功能)")
        print("=" * 60)
        print()
    
    def process(self, user_input: str) -> dict:
        """处理用户输入"""
        
        self.logger.info(f"处理用户输入: {user_input[:50]}...", module="main")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 收到请求，开始处理...")
        print()
        
        print("Step 1: 意图分析...")
        intent_result = self.intent_analyzer.analyze(user_input)
        print(f"  意图: {intent_result['intent']}")
        print(f"  置信度: {intent_result['confidence']:.2%}")
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
        
        hook_manager.execute("pre_workflow", {
            "workflow": workflow,
            "intent": intent_result,
            "scenario": scenario
        })
        
        print("Step 4: 工作流执行...")
        context = {
            "user_input": user_input,
            "intent": intent_result,
            "scenario": scenario
        }
        workflow_result = self.workflow_engine.execute_workflow(workflow, context)
        print(f"  状态: {workflow_result['status']}")
        print()
        
        if workflow_result['status'] == 'failed':
            hook_manager.execute("on_error", {
                "workflow": workflow,
                "error": workflow_result.get('error'),
                "step": workflow_result.get('failed_step')
            })
        
        print("Step 5: 零件提取...")
        parts_result = auto_collect_parts(self.parts_library, workflow_result)
        print(f"  提取零件: {parts_result['added']}个")
        print()
        
        print("Step 6: 系统进化...")
        evolution_result = self.evolution_engine.evolve_after_interaction({
            "id": datetime.now().strftime('%Y%m%d%H%M%S'),
            "scenario": scenario['name'],
            "intent": intent_result['intent'],
            "skills_used": scenario['required_skills'],
            "success": workflow_result['status'] == 'completed',
            "parts_extracted": parts_result['added'],
            "keywords": intent_result.get('keywords', [])
        })
        print(f"  进化状态: 完成")
        print()
        
        hook_manager.execute("post_workflow", {
            "workflow_result": workflow_result,
            "evolution_result": evolution_result
        })
        
        print("Step 7: 结果输出...")
        output = self._generate_output(workflow_result, scenario)
        print(f"  输出目录: {output['output_dir']}")
        print()
        
        print("Step 8: 持续优化...")
        optimization_result = self.continuous_optimizer.run_optimization_cycle()
        if optimization_result['improvements']:
            print(f"  检测到 {len(optimization_result['improvements'])} 个改进点")
            print(f"  应用了 {len(optimization_result['applied'])} 个改进")
        print()
        
        return {
            "intent": intent_result,
            "scenario": scenario,
            "workflow": workflow_result,
            "parts": parts_result,
            "evolution": evolution_result,
            "output": output,
            "optimization": optimization_result
        }
    
    def _generate_output(self, workflow_result: dict, scenario: dict) -> dict:
        """生成输出"""
        
        scenario_name = scenario.get("name", "通用场景")
        output_dir = self.output_manager.create_output_dir(scenario_name)
        
        output_file = output_dir / "result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(workflow_result, f, ensure_ascii=False, indent=2)
        
        self.output_manager.add_file(output_dir.name, str(output_file))
        
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
                print("处理完成!")
                print("-" * 60)
                print()
                
            except KeyboardInterrupt:
                print("\n感谢使用，再见！")
                break
            except Exception as e:
                self.logger.error(f"处理错误: {e}", module="main")
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
            "监测": self._cmd_news_monitor,
            "统计": self._cmd_stats,
            "进化": self._cmd_evolution,
            "优化": self._cmd_optimization,
            "健康": self._cmd_health,
            "loop": self._cmd_loop,
            "调度": self._cmd_schedule,
            "学习": self._cmd_learning,
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
    
    def _cmd_news_monitor(self, params: str):
        """新闻监测命令"""
        user_input = f"监测{params}新闻动态"
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
        print(f"  自动适应: {evolution_report['metrics']['auto_adaptations']}次")
        print(f"  模式发现: {evolution_report['metrics']['pattern_discoveries']}个")
        print()
    
    def _cmd_evolution(self, params: str):
        """进化命令"""
        
        if params == "auto":
            print("执行自动进化...")
            result = self.evolution_engine.auto_evolve()
            print(f"分析模式数: {result['patterns_analyzed']}")
            print(f"执行动作: {len(result['actions'])}个")
            for action in result['actions']:
                print(f"  - {action['action']}: {action.get('scenario', '')}")
        else:
            patterns = self.evolution_engine.analyze_patterns()
            print("使用模式分析:")
            print(f"  常见意图: {list(patterns['common_intents'].keys())[:5]}")
            print(f"  常见场景: {list(patterns['common_scenarios'].keys())[:5]}")
            print(f"  技能使用: {list(patterns['skill_usage'].keys())[:5]}")
            
            suggestions = self.evolution_engine.suggest_improvements()
            if suggestions:
                print("\n改进建议:")
                for s in suggestions:
                    print(f"  - [{s['type']}] {s['suggestion']}")
    
    def _cmd_optimization(self, params: str):
        """优化命令"""
        
        print("运行持续优化循环...")
        result = self.continuous_optimizer.run_optimization_cycle()
        
        print(f"检测到 {len(result['improvements'])} 个改进点")
        for imp in result['improvements']:
            print(f"  - [{imp['priority']}] {imp['suggestion']}")
        
        print(f"应用了 {len(result['applied'])} 个改进")
        print()
    
    def _cmd_health(self, params: str):
        """健康检查命令"""
        
        health = self.evolution_monitor.get_system_health()
        
        print("系统健康状态:")
        print(f"  状态: {health['status']}")
        print(f"  时间: {health['timestamp']}")
        
        if health['alerts']:
            print("\n告警:")
            for alert in health['alerts']:
                print(f"  - [{alert['level']}] {alert['message']}")
        
        if health['recommendations']:
            print("\n建议:")
            for rec in health['recommendations']:
                print(f"  - {rec['message']}")
        
        print()
    
    def _cmd_loop(self, params: str):
        """自动化循环命令"""
        
        if params == "start":
            print("启动自动化循环引擎...")
            interval = 60
            self.auto_loop_engine.start(interval=interval)
            
            try:
                while self.auto_loop_engine.running:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n停止自动化循环...")
                self.auto_loop_engine.stop()
        
        elif params == "stop":
            self.auto_loop_engine.stop()
        
        elif params == "once":
            self.auto_loop_engine.run_once()
        
        elif params == "status":
            status = self.auto_loop_engine.get_status()
            print("自动化循环状态:")
            print(f"  运行状态: {'运行中' if status['running'] else '已停止'}")
            print(f"  当前迭代: #{status['current_iteration']}")
            print(f"  队列大小: {status['queue_size']}")
            print(f"  循环间隔: {status['loop_interval']}秒")
            print(f"\n统计信息:")
            print(f"  总循环数: {status['stats']['total_loops']}")
            print(f"  任务完成: {status['stats']['tasks_completed']}")
            print(f"  任务失败: {status['stats']['tasks_failed']}")
            print(f"  学习事件: {status['stats']['learning_events']}")
            print(f"  优化应用: {status['stats']['optimizations_applied']}")
        
        else:
            print("自动化循环引擎命令:")
            print("  /loop start  - 启动自动循环")
            print("  /loop stop   - 停止自动循环")
            print("  /loop once   - 执行一次循环")
            print("  /loop status - 查看循环状态")
    
    def _cmd_schedule(self, params: str):
        """任务调度命令"""
        
        if params.startswith("add "):
            parts = params[4:].split(" ", 2)
            if len(parts) >= 2:
                task_type = parts[0]
                delay_seconds = int(parts[1])
                task_data = json.loads(parts[2]) if len(parts) > 2 else {}
                
                from datetime import datetime, timedelta
                schedule_time = datetime.now() + timedelta(seconds=delay_seconds)
                
                task_id = f"scheduled_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.workflow_scheduler.schedule_task(
                    task_id=task_id,
                    task_type=task_type,
                    schedule_time=schedule_time,
                    data=task_data
                )
            else:
                print("用法: /调度 add <任务类型> <延迟秒数> [JSON数据]")
        
        elif params == "list":
            pending = self.workflow_scheduler.get_pending_tasks()
            print(f"待执行任务: {len(pending)}个")
            for task in pending[:10]:
                print(f"  - {task['task_id']} ({task['task_type']})")
        
        elif params == "stats":
            stats = self.workflow_scheduler.get_scheduler_stats()
            print("调度器统计:")
            print(f"  总调度: {stats['total_scheduled']}")
            print(f"  已完成: {stats['completed']}")
            print(f"  已失败: {stats['failed']}")
            print(f"  待执行: {stats['pending']}")
        
        else:
            print("任务调度命令:")
            print("  /调度 add <类型> <延迟> [数据] - 添加调度任务")
            print("  /调度 list                    - 列出待执行任务")
            print("  /调度 stats                   - 查看调度统计")
    
    def _cmd_learning(self, params: str):
        """持续学习命令"""
        
        if params == "report":
            report = self.continuous_learning.get_learning_report()
            print("学习报告:")
            print(f"  总模式数: {report['stats']['total_patterns']}")
            print(f"  模式应用: {report['stats']['patterns_applied']}")
            print(f"  学习事件: {report['stats']['learning_events']}")
            print(f"  改进次数: {report['stats']['improvements']}")
            
            print(f"\n模式类型分布:")
            for ptype, count in report['pattern_types'].items():
                print(f"  {ptype}: {count}个")
            
            print(f"\nTop 10 模式:")
            for i, pattern in enumerate(report['top_patterns'], 1):
                print(f"  {i}. {pattern['pattern_id']} (置信度: {pattern['confidence']:.2%}, 使用: {pattern['usage']})")
        
        elif params == "evolve":
            self.continuous_learning.evolve_patterns()
        
        elif params == "skills":
            skills = self.continuous_learning.generate_skill_from_patterns()
            if skills:
                print(f"可生成技能: {len(skills)}个")
                for skill in skills:
                    print(f"  - {skill['skill_name']} (置信度: {skill['confidence']:.2%})")
            else:
                print("暂无可生成技能")
        
        else:
            print("持续学习命令:")
            print("  /学习 report  - 查看学习报告")
            print("  /学习 evolve  - 进化学习模式")
            print("  /学习 skills  - 生成新技能")
    
    def _cmd_help(self, params: str):
        """帮助命令"""
        
        print("可用命令:")
        print()
        print("  /谋划 <项目描述>  - 项目谋划")
        print("  /筛选 <项目列表>  - 项目筛选")
        print("  /研究 <政策关键词> - 政策研究")
        print("  /组装 <主题>      - 快速组装")
        print("  /宣讲 <主题>      - 生成宣讲PPT")
        print("  /监测 <关键词>    - 新闻监测")
        print("  /统计            - 查看系统统计")
        print("  /进化 [auto]      - 进化分析/自动进化")
        print("  /优化            - 运行持续优化")
        print("  /健康            - 系统健康检查")
        print("  /loop start      - 启动自动化循环")
        print("  /loop stop       - 停止自动化循环")
        print("  /loop once       - 执行一次循环")
        print("  /loop status     - 查看循环状态")
        print("  /调度 add/list/stats - 任务调度")
        print("  /学习 report/evolve/skills - 持续学习")
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

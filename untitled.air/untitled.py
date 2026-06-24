__author__ = "platypus"
from airtest.core.api import *
auto_setup(__file__)

CONFIRM_BTN = (Template(r"tpl1776261133078.png", record_pos=(0.208, 0.26), resolution=(578, 1304)))
X_BTN = (Template(r"tpl1774938679692.png", record_pos=(0.398, -0.68), resolution=(578, 1312)))
CANCEL_BTN = (Template(r"tpl1775726421996.png", record_pos=(-0.268, 0.512), resolution=(578, 1304)))
HOME_BTN = (Template(r"tpl1776348835527.png", record_pos=(-0.227, 1.067), resolution=(578, 1350)))
REWARD_BTN = (Template(r"tpl1775048235567.png", record_pos=(0.004, -0.293), resolution=(562, 1311)))

def close_if_exists(template):
    target = exists(template)
    if target:
        touch(target)
        sleep(1.0)
        return True
    return False

def close_all_popups(*templates, max_attempts=10):
    """여러 팝업이 연속으로 떠도 모두 닫힐 때까지 반복 처리"""
    for _ in range(max_attempts):
        closed_any = False
        for t in templates:
            if close_if_exists(t):
                closed_any = True
        if not closed_any:
            break

def wait_and_touch(template, timeout=5.5):
    try:
        target = wait(template, timeout=timeout)
        touch(target)
        sleep(0.5)
        return True
    except Exception as e:
        print(f"[WARN] wait_and_touch 실패: {e}")
        return False

def wait_and_touch_any(*templates, timeout=10):
    import time
    start = time.time()
    while time.time() - start < timeout:
        for t in templates:
            target = exists(t)
            if target:
                touch(target)
                sleep(0.5)
                return True
    print("[WARN] wait_and_touch_any 실패")
    return False

def purchase_flow(item_template, confirm_template):
    wait_and_touch(item_template)
    wait_and_touch(confirm_template)
    close_all_popups(REWARD_BTN)

def run_enter():
    # 게임 진입 부분
    wait_and_touch(Template(r"tpl1775547357047.png", record_pos=(0.071, 0.106), resolution=(578, 1304)))
    sleep(3.3)
    close_all_popups(X_BTN)
    sleep(1.5)

def run_friend():
    # 친구 / 주고받는 부분
    wait_and_touch(Template(r"tpl1774939197911.png", record_pos=(0.412, -0.696), resolution=(578, 1304)))
    sleep(1.0)
    active = exists(Template(r"tpl1775725193484.png", record_pos=(0.263, 0.663), resolution=(578, 1304)))
    inactive = exists(Template(r"tpl1775564601039.png", record_pos=(0.265, 0.661), resolution=(578, 1304)))

    print(f"[DEBUG] active: {active}")
    print(f"[DEBUG] inactive: {inactive}")

    if active:
        touch(active)
        sleep(1.5)
        close_if_exists(CONFIRM_BTN)
        close_if_exists(X_BTN)
    else:
        if inactive:
            close_if_exists(X_BTN)

def run_outpost():
    # 전초기지 방어 받는 부분
    wait_and_touch_any(
        Template(r"tpl1774939393128.png", record_pos=(-0.362, 0.869), resolution=(578, 1350)),
        Template(r"tpl1775048200038.png", record_pos=(-0.363, 0.866), resolution=(562, 1311))
    )
    close_if_exists(CONFIRM_BTN)
    wait_and_touch(Template(r"tpl1774939442260.png", record_pos=(-0.199, 0.628), resolution=(578, 1350)))
    sleep(1.6)

    has_cost_BTN = exists(Template(r"tpl1775728975672.png", record_pos=(0.147, 0.512), resolution=(578, 1304)))
    if has_cost_BTN:
        # 재화 써야하면 → 취소
        close_if_exists(CANCEL_BTN)
    else:
        # 무료 → 섬멸 진행
        active_destroy = exists(Template(r"tpl1774939487578.png", record_pos=(0.263, 0.472), resolution=(578, 1350)))
        if active_destroy:
            touch(active_destroy)
            close_all_popups(REWARD_BTN)
            close_if_exists(CANCEL_BTN)

    wait_and_touch(Template(r"tpl1775725715679.png", record_pos=(0.201, 0.67), resolution=(578, 1304)))
    close_all_popups(REWARD_BTN)

def run_shop():
    # 상점 구매 부분
    wait_and_touch(Template(r"tpl1775048609423.png", record_pos=(-0.311, 0.617), resolution=(562, 1311)))
    sold_out = exists(Template(r"tpl1776260286036.png", record_pos=(-0.197, -0.059), resolution=(578, 1304)))
    if not sold_out:
        purchase_flow(
            Template(r"tpl1775048680212.png", record_pos=(-0.198, 0.058), resolution=(562, 1311)),
            Template(r"tpl1775048700799.png", record_pos=(0.155, 0.602), resolution=(562, 1311))
        )
    wait_and_touch(Template(r"tpl1776341272202.png", record_pos=(-0.247, -0.314), resolution=(578, 1295)))

    # 0원이면 확인 후 구매, 아니면 취소
    free_refresh = exists(Template(r"tpl1776410497524.png", record_pos=(0.076, 0.106), resolution=(578, 1296)))
    if free_refresh:
        wait_and_touch(CONFIRM_BTN)
        purchase_flow(
            Template(r"tpl1775048680212.png", record_pos=(-0.198, 0.058), resolution=(562, 1311)),
            Template(r"tpl1775048700799.png", record_pos=(0.155, 0.602), resolution=(562, 1311))
        )
    else:
        wait_and_touch(CANCEL_BTN)
    wait_and_touch(HOME_BTN)

def run_dispatch():
    # 전초기지 파견 부분
    wait_and_touch(Template(r"tpl1776264582620.png", record_pos=(-0.253, 0.763), resolution=(578, 1350)))
    sleep(1.5)
    wait_and_touch(Template(r"tpl1776264647292.png", record_pos=(0.069, 1.083), resolution=(578, 1350)))
    sleep(1.0)

    # 파란색(active) 먼저 체크
    active_receive = exists(Template(r"tpl1776264706936.png", record_pos=(0.284, 0.651), resolution=(578, 1295)))
    print(f"[DEBUG] active_receive: {active_receive}")
    if active_receive:
        # 파란색 → 수령 후 파견
        touch(active_receive)
        sleep(1.0)
        close_all_popups(REWARD_BTN)
        sleep(1.0)
        wait_and_touch(Template(r"tpl1776264895209.png", record_pos=(-0.002, 0.653), resolution=(578, 1295)))
        sleep(1.0)
        wait_and_touch(Template(r"tpl1776264925767.png", record_pos=(0.133, 0.657), resolution=(578, 1295)))
        sleep(1.0)
        close_if_exists(Template(r"tpl1776341212824.png", record_pos=(0.41, -0.651), resolution=(578, 1350)))
    else:
        # 파란색 없으면 → X 버튼 누르고 나가기
        close_if_exists(Template(r"tpl1776341212824.png", record_pos=(0.41, -0.651), resolution=(578, 1350)))

    wait_and_touch(HOME_BTN)

def run_interception():
    # 요격전 부분
    wait_and_touch(Template(r"tpl1776344309017.png", record_pos=(0.279, 0.634), resolution=(578, 1295)))
    sleep(3.0)
    wait_and_touch(Template(r"tpl1776402715421.png", record_pos=(-0.215, 0.48), resolution=(578, 1295)))
    sleep(3.0)
    touch((288, 987))
    sleep(3.0)
    # 3/3 이면 전투 진입, 아니면 주간 빠른 전투
    count_full = exists(Template(r"tpl1780035591058.png", record_pos=(0.244, 1.059), resolution=(578, 1350)))
    if count_full:
        wait_and_touch(Template(r"tpl1776402813539.png", record_pos=(0.244, 1.012), resolution=(578, 1350)))
        sleep(3.0)
        import time
        start = time.time()
        while time.time() - start < 240:
            battle_end = exists(Template(r"tpl1776402986760.png", record_pos=(-0.002, 0.958), resolution=(578, 1350)))
            if battle_end:
                touch(battle_end)
                sleep(3.0)
                for _ in range(3):
                    btn = exists(Template(r"tpl1778763659308.png", record_pos=(0.315, 0.882), resolution=(578, 1350)))
                    if btn:
                        touch(btn)
                        sleep(3.0)
                        close_if_exists(Template(r"tpl1776402986760.png", record_pos=(-0.002, 0.958), resolution=(578, 1350)))
                        sleep(3.0)
                    else:
                        break
                break
            sleep(3.5)
    else:
        for _ in range(3):
            btn = exists(Template(r"tpl1778763659308.png", record_pos=(0.315, 0.882), resolution=(578, 1350)))
            if btn:
                touch(btn)
                sleep(3.0)
                close_if_exists(Template(r"tpl1776402986760.png", record_pos=(-0.002, 0.958), resolution=(578, 1350)))
                sleep(3.0)
            else:
                break
    wait_and_touch(HOME_BTN)
    
def run_mission():
    # 퀘스트 보상 받는 부분
    wait_and_touch(Template(r"tpl1776412363668.png", record_pos=(0.088, -0.943), resolution=(578, 1296)))
    sleep(2.0)

    # 모두받기 버튼 있는 동안 반복 (최대 5번)
    for _ in range(2):
        btn = exists(Template(r"tpl1776412401468.png", record_pos=(0.298, 0.754), resolution=(578, 1296)))
        if btn:
            touch(btn)
            sleep(2.0)
            close_all_popups(REWARD_BTN)
            sleep(2.0)
        else:
            break

    close_if_exists(X_BTN)

def run():
    #run_enter() #로비 진입 부분은 필수라 처음 실행 때 주석처리 금지!
    #run_friend()
    #run_outpost()
    #run_shop()
    #run_dispatch()
    #run_simulation()
    run_interception()
    #run_mission()
    

run()
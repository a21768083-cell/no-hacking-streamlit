import random
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="에러를 잡아라!", page_icon="🚨", layout="centered")

# 세션 상태(변수) 초기화
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.hp = 100
    st.session_state.progress = 0
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.session_state.ending_msg = ""

    # 에러 리스트 초기화
    st.session_state.errors = [
        "❌ NameError: name 'user_id' is not defined",
        "❌ IndexError: list index out of range",
        "❌ ZeroDivisionError: division by zero",
        "❌ IndentationError: unexpected indent",
        "❌ TypeError: can only concatenate str (not 'int') to str",
    ]
    random.shuffle(st.session_state.errors)


# 새로운 턴(문제) 생성 함수
def generate_new_problem():
    if not st.session_state.errors:
        st.session_state.game_over = True
        return

    st.session_state.current_error = st.session_state.errors.pop()
    st.session_state.num_math_questions = random.randint(2, 5)
    st.session_state.math_questions = []

    # 필요한 개수만큼 수학 문제 미리 생성
    for _ in range(st.session_state.num_math_questions):
        op = random.choice(["+", "-", "*", "/"])
        if op == "+":
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            ans = num1 + num2
        elif op == "-":
            num1 = random.randint(5, 15)
            num2 = random.randint(1, num1)
            ans = num1 - num2
        elif op == "*":
            num1 = random.randint(2, 9)
            num2 = random.randint(1, 9)
            ans = num1 * num2
        elif op == "/":
            num2 = random.randint(2, 5)
            ans = random.randint(1, 5)
            num1 = num2 * ans

        st.session_state.math_questions.append(
            {"question": f"{num1} {op} {num2}", "answer": ans}
        )


# 첫 문제 생성
if "current_error" not in st.session_state and not st.session_state.game_over:
    generate_new_problem()

# --- 화면 UI 그리기 ---
st.title("🚨 프로젝트 마감 1시간 전! 에러를 잡아라!")
st.caption(
    "당신은 지금 출시 직전의 서비스 코드를 수정하고 있습니다. 밀려오는 에러를 해결하고 퇴근하세요!"
)
st.write("---")

# 엔딩 체크
if st.session_state.progress >= 100:
    st.balloons()
    st.success(
        "🎉 축하합니다! 정시 퇴근 성공! 당신은 최고의 시니어 개발자입니다! 👑"
    )
    st.session_state.game_over = True
elif st.session_state.hp <= 0:
    st.error("💀 멘탈이 버티지 못하고 터졌습니다... 야근 확정 (Bad Ending)")
    st.session_state.game_over = True
elif st.session_state.game_over and st.session_state.progress < 100:
    st.warning(
        "🚧 완성도가 부족한 채로 출시되어 서버가 터졌습니다... (Normal Ending)"
    )

# 게임 진행 중일 때의 화면
if not st.session_state.game_over:
    # 상단 상태바
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🧠 현재 멘탈", value=f"{st.session_state.hp}%")
    with col2:
        st.metric(label="🛠️ 프로젝트 완성도", value=f"{st.session_state.progress}%")

    st.subheader(f"🔥 [버그 해결 {st.session_state.turn}단계]")
    st.error(f"**[⚠️ 경고 메시지 발생!]**\n\n{st.session_state.current_error}")

    st.info(
        f"🔓 디버깅을 하려면 아래 【 {st.session_state.num_math_questions}개 】의 연산 암호를 모두 맞혀야 합니다!"
    )

    # 입력 폼 생성
    with st.form(key="math_form", clear_on_submit=True):
        user_answers = []
        for i, q in enumerate(st.session_state.math_questions):
            ans_input = st.number_input(
                f"👉 [암호 {i+1}] {q['question']} = ?",
                step=1,
                value=0,
                key=f"q_{st.session_state.turn}_{i}",
            )
            user_answers.append(ans_input)

        submit_button = st.form_submit_button(label="코드 수정 완료 (제출)")

    if submit_button:
        # 정답 확인
        success_all = True
        for i, q in enumerate(st.session_state.math_questions):
            if user_answers[i] != q["answer"]:
                success_all = False
                break

        if success_all:
            st.toast("정답입니다! 완성도 +25%", icon="✅")
            st.session_state.progress += 25
        else:
            st.toast("오답이 있습니다! 멘탈 -20", icon="❌")
            st.session_state.hp -= 20

        # 다음 턴으로 넘어가기
        st.session_state.turn += 1
        generate_new_problem()
        st.rerun()

# 게임 리셋 버튼
if st.session_state.game_over:
    if st.button("게임 다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

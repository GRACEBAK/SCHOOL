import streamlit as st
import random

# 짝짓기 문제 목록 (대문자:소문자)
# A-Z 중 5개를 무작위로 선택하도록 할게요.
ALL_PAIRS = {
    'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g', 'H': 'h', 'I': 'i',
    'J': 'j', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'O': 'o', 'P': 'p', 'Q': 'q', 'R': 'r',
    'S': 's', 'T': 't', 'U': 'u', 'V': 'v', 'W': 'w', 'X': 'x', 'Y': 'y', 'Z': 'z'
}

def generate_questions(num_questions=5):
    """5개의 무작위 대소문자 짝짓기 문제를 생성합니다."""
    # 전체 쌍에서 5개 쌍을 무작위로 선택
    selected_capital_letters = random.sample(list(ALL_PAIRS.keys()), num_questions)
    
    # 문제 형식: {'대문자': '정답 소문자'}
    questions = {cap: ALL_PAIRS[cap] for cap in selected_capital_letters}
    return questions

def display_game():
    """Streamlit을 이용해 게임 화면을 구성합니다."""
    st.set_page_config(page_title="알파벳 짝짓기 게임", layout="centered")
    
    st.title("⭐ 알파벳 대소문자 짝짓기 게임! ⭐")
    st.markdown("---")
    
    # 세션 상태 초기화 (게임이 시작되었는지, 점수, 문제 목록)
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = {}
    if 'attempts' not in st.session_state:
        st.session_state.attempts = {} # {대문자: 사용자가 선택한 소문자}

    # === 게임 시작 화면 ===
    if not st.session_state.game_started:
        st.write("안녕, 친구들! 👋 **대문자**와 짝이 되는 **소문자**를 잘 알고 있는지 확인해 볼까요?")
        st.write("아래 **'게임 시작!'** 버튼을 누르고, 나오는 5문제의 짝을 찾아 연결해 주세요!")
        if st.button("🚀 게임 시작!"):
            st.session_state.questions = generate_questions(5)
            st.session_state.score = 0
            st.session_state.attempts = {}
            st.session_state.game_started = True
            # Streamlit은 상태가 변경되면 다시 실행되므로, 이 코드는 재실행을 유발합니다.
            st.rerun()

    # === 게임 진행 화면 ===
    elif st.session_state.game_started and st.session_state.questions:
        st.subheader("💡 짝이 되는 소문자를 찾아 선택해 보세요.")
        
        # 1. 정답 선택지 목록 (보기) 생성
        correct_answers = list(st.session_state.questions.values()) # 정답 소문자 5개
        
        # 오답을 추가하여 선택지를 8~10개 정도로 만듭니다.
        # 정답이 아닌 소문자들만 모아서 오답 풀을 만들고, 그중 일부를 선택합니다.
        incorrect_pool = [v for k, v in ALL_PAIRS.items() if v not in correct_answers]
        num_incorrect = 5 # 오답 5개를 추가
        incorrect_options = random.sample(incorrect_pool, num_incorrect)
        
        # 전체 선택지 (정답 5개 + 오답 5개 = 총 10개)
        all_options = correct_answers + incorrect_options
        random.shuffle(all_options) # 선택지를 무작위로 섞음

        # 문제 번호
        question_number = 1
        
        # 문제를 하나씩 표시하고 사용자의 선택을 받습니다.
        for capital_letter, correct_small in st.session_state.questions.items():
            
            # 현재 문제의 소문자가 선택지 목록에 있는지 확인
            # (위에 all_options에 추가했기 때문에 항상 있을 거예요.)
            
            # 사용자에게 드롭다운(select box)으로 소문자를 선택하게 합니다.
            # 기본값은 '선택'으로 설정
            current_choice = st.session_state.attempts.get(capital_letter, '선택')
            
            # 선택지 목록 앞에 '선택' 추가
            options_with_default = ['선택'] + all_options
            
            # 대문자를 크게 표시
            st.markdown(f"**{question_number}.** <span style='font-size: 30px; color: #FF4B4B;'>**{capital_letter}**</span> 와 짝은?", unsafe_allow_html=True)
            
            # 사용자 선택 저장
            # key를 사용해 각 selectbox가 독립적으로 작동하도록 합니다.
            selected_answer = st.selectbox(
                f"**{capital_letter}**의 짝은?", 
                options_with_default,
                key=f"q_{capital_letter}",
                index=options_with_default.index(current_choice) if current_choice in options_with_default else 0,
                label_visibility='collapsed' # 레이블 숨기기
            )
            
            if selected_answer != '선택':
                st.session_state.attempts[capital_letter] = selected_answer
            
            question_number += 1
            st.markdown("---")


        # === 채점 버튼 ===
        if st.button("🎉 채점하기!"):
            score = 0
            feedback = []
            
            # 모든 문제를 풀었는지 확인
            if len(st.session_state.attempts) < 5 or '선택' in st.session_state.attempts.values():
                st.warning("아직 풀지 않은 문제가 있어요. 모든 문제의 짝을 선택해 주세요!")
            else:
                # 채점 로직
                for capital, correct_small in st.session_state.questions.items():
                    user_answer = st.session_state.attempts[capital]
                    
                    if user_answer == correct_small:
                        score += 1
                        feedback.append(f"✅ **{capital}**의 짝은 **{correct_small}**! (정답!)")
                    else:
                        feedback.append(f"❌ **{capital}**의 짝은 **{user_answer}**가 아니라 **{correct_small}**예요. (오답)")
                        
                st.session_state.score = score
                st.session_state.game_started = False # 게임 종료 상태로 전환
                st.session_state.feedback = feedback
                st.rerun() # 결과 화면으로 넘어가기 위해 재실행

    # === 게임 결과 화면 ===
    elif not st.session_state.game_started and 'feedback' in st.session_state:
        
        if st.session_state.score == 5:
            st.balloons()
            st.success("🥇 와! 우리 친구 정말 대단해요! **5문제 모두 정답**이에요! 💯")
        elif st.session_state.score >= 3:
            st.info(f"🌟 잘 했어요! **5개 중에 {st.session_state.score}개** 맞췄네요! 조금만 더 하면 완벽해질 수 있어요! 💪")
        else:
            st.warning(f"😔 괜찮아요! **5개 중에 {st.session_state.score}개** 맞췄네요. 다음엔 더 잘할 수 있을 거예요. 우리 **대문자**와 **소문자**를 다시 복습해 봐요! 책을 펼쳐 볼까요? 📖")
            
        st.subheader("📝 채점 결과:")
        for line in st.session_state.feedback:
            st.markdown(line)
        
        st.markdown("---")
        
        if st.button("🔄 다시 게임하기!"):
            # 상태 초기화 후 재시작
            st.session_state.game_started = True
            st.session_state.questions = generate_questions(5)
            st.session_state.score = 0
            st.session_state.attempts = {}
            if 'feedback' in st.session_state:
                del st.session_state.feedback
            st.rerun()


# Streamlit 앱 실행
if __name__ == "__main__":
    # st.session_state가 제대로 작동하려면 이 코드가 직접 실행되어야 합니다.
    display_game()

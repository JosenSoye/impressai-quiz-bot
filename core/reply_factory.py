
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    try:
        new_answer = answer(
            question_id=current_question_id,
            answer_text=answer,
            
        )
        session.add(new_answer)
        session.commit()
        return True
    except Exception as e:
        session.rollback() 
        print(f"An error occurred while recording the answer: {e}")
        return False
    



def get_next_question(current_question_id):
    try:
        questions = [
         get.PYTHON_QUESTION_LIST            
        ]
        current_index = next((index for index, q in enumerate(questions) if q['id'] == current_question_id), None)

        if current_index is not None and current_index + 1 < len(questions):
            next_question = questions[current_index + 1]
            return next_question["text"], next_question["id"]
        else:
            return "No more questions", -1
    except Exception as e:
        print(f"An error occurred while fetching the next question: {e}")
        return "Error fetching question", -1




def generate_final_response(session):
    try:
        PYTHON_QUESTION_LIST = [
            get.PYTHON_QUESTION_LIST
        ]

        user_answers = session.query(Answer).all()

        
        score = 0
        total_questions = len(PYTHON_QUESTION_LIST)
        for question in PYTHON_QUESTION_LIST:
            user_answer = next((a for a in user_answers if a.question_id == question["id"]), None)
            if user_answer and user_answer.answer_text.strip().lower() == question["correct_answer"].strip().lower():
                score += 1

        
        result_message = f"Your final score is {score}/{total_questions}.\n"
        if score == total_questions:
            result_message += "Excellent! You got everything right."
        elif score > total_questions // 2:
            result_message += "Good job! You answered most questions correctly."
        else:
            result_message += "Keep practicing! You'll improve with more effort."

        return result_message
    except Exception as e:
        print(f"An error occurred while generating the final response: {e}")
        return "Error generating the final result."




const questionReactions = document.getElementsByClassName(
  "reaction-container-question"
);
const answerReactions = document.getElementsByClassName(
  "reaction-container-answer"
);

const addReactQuestion = (btn, countEl, id, type) => {
  const formData = new FormData();
  formData.append("question_id", id);
  formData.append("type", type);

  const request = new Request("/question/like", {
    method: "POST",
    body: formData,
  });

  fetch(request)
    .then((res) => res.json())
    .then((data) => {
      countEl.innerHTML = data.count;
      btn.style.style = "stroke: blue";
      btn.style.fill = "blue";
    });
};

const addReactAnswer = (countEl, id, type) => {
  const formData = new FormData();
  formData.append("answer_id", id);
  formData.append("type", type);

  const request = new Request("/answer/like", {
    method: "POST",
    body: formData,
  });

  fetch(request)
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      countEl.innerHTML = data.count;
    });
};

if (questionReactions.length) {
  for (let i = 0; i < questionReactions.length; ++i) {
    let reaction = questionReactions[i];
    let like = reaction.children[0];
    let count = reaction.children[1];
    let dislike = reaction.children[2];
    path = like.children[0].children[0];
    let questionId = reaction.getAttribute("question-id");
    like.addEventListener("click", () => {
      addReactQuestion(path, count, questionId, "like");
    });
    dislike.addEventListener("click", () => {
      addReactQuestion(path, count, questionId, "dislike");
    });
  }
}

if (answerReactions.length) {
  for (let i = 0; i < answerReactions.length; ++i) {
    let reaction = answerReactions[i];
    let like = reaction.children[0];
    let count = reaction.children[1];
    let dislike = reaction.children[2];
    let answerId = reaction.getAttribute("answer-id");
    like.addEventListener("click", () => {
      addReactAnswer(count, answerId, "like");
    });
    dislike.addEventListener("click", () => {
      addReactAnswer(count, answerId, "dislike");
    });
  }
}

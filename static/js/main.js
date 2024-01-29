const questionReactions = document.getElementsByClassName(
  "reaction-container-question"
);
const answerReactions = document.getElementsByClassName(
  "reaction-container-answer"
);

const addReactQuestion = (like, dislike, countEl, id, type) => {
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
      if (type == "like" && countEl.innerHTML > data.count)
        like.src = "/static/svg/like.svg";
      if (type == "like" && countEl.innerHTML < data.count) {
        like.src = "/static/svg/like_clicked.svg";
        dislike.src = "/static/svg/dislike.svg";
      }
      if (type == "dislike" && countEl.innerHTML < data.count)
        dislike.src = "/static/svg/dislike.svg";
      if (type == "dislike" && countEl.innerHTML > data.count) {
        dislike.src = "/static/svg/dislike_clicked.svg";
        like.src = "/static/svg/like.svg";
      }

      countEl.innerHTML = data.count;
    });
};

const addReactAnswer = (like, dislike, countEl, id, type) => {
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
      if (type == "like" && countEl.innerHTML > data.count)
        like.src = "/static/svg/like.svg";
      if (type == "like" && countEl.innerHTML < data.count) {
        like.src = "/static/svg/like_clicked.svg";
        dislike.src = "/static/svg/dislike.svg";
      }
      if (type == "dislike" && countEl.innerHTML < data.count)
        dislike.src = "/static/svg/dislike.svg";
      if (type == "dislike" && countEl.innerHTML > data.count) {
        dislike.src = "/static/svg/dislike_clicked.svg";
        like.src = "/static/svg/like.svg";
      }

      countEl.innerHTML = data.count;
    });
};

if (questionReactions.length) {
  for (let i = 0; i < questionReactions.length; ++i) {
    let reaction = questionReactions[i];
    let like = reaction.children[0];
    let count = reaction.children[1];
    let dislike = reaction.children[2];
    let likeImg = like.children[0];
    let dislikeImg = dislike.children[0];
    let questionId = reaction.getAttribute("question-id");
    like.addEventListener("click", () => {
      addReactQuestion(likeImg, dislikeImg, count, questionId, "like");
    });
    dislike.addEventListener("click", () => {
      addReactQuestion(likeImg, dislikeImg, count, questionId, "dislike");
    });
  }
}

if (answerReactions.length) {
  for (let i = 0; i < answerReactions.length; ++i) {
    let reaction = answerReactions[i];
    let like = reaction.children[0];
    let count = reaction.children[1];
    let dislike = reaction.children[2];
    let likeImg = like.children[0];
    let dislikeImg = dislike.children[0];
    let answerId = reaction.getAttribute("answer-id");
    like.addEventListener("click", () => {
      addReactAnswer(likeImg, dislikeImg, count, answerId, "like");
    });
    dislike.addEventListener("click", () => {
      addReactAnswer(likeImg, dislikeImg, count, answerId, "dislike");
    });
  }
}

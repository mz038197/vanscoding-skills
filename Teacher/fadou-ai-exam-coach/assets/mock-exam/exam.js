(function () {
  "use strict";

  var dataEl = document.getElementById("exam-data");
  var examData;
  try {
    examData = JSON.parse(dataEl.textContent);
  } catch (e) {
    document.body.innerHTML = "<p style='padding:2rem'>無法載入試卷資料。</p>";
    return;
  }

  var questions = examData.questions || [];
  var passScore = examData.passScore != null ? examData.passScore : 70;
  var sessionId = examData.sessionId || "default";
  var formEl = document.getElementById("exam-form");
  var progressText = document.getElementById("progress-text");
  var progressFill = document.getElementById("progress-fill");
  var submitBtn = document.getElementById("submit-btn");
  var resultsEl = document.getElementById("results");
  var footerEl = document.querySelector(".footer");
  var headerEl = document.querySelector(".header");

  var currentAttempt = getAttempt();

  var CATEGORY_RANGES = [
    { name: "AI 倫理與社會影響", start: 1, end: 10 },
    { name: "Python 基礎運用", start: 11, end: 20, alt: "AI 程式語言" },
    { name: "人工智慧理論知識", start: 21, end: 30 },
    { name: "人工智慧技術運用", start: 31, end: 50 }
  ];

  function attemptKey() {
    return "fadou-mock-attempt:" + sessionId;
  }

  function draftKey() {
    return "fadou-mock-draft:" + sessionId + ":" + currentAttempt;
  }

  function resultKey() {
    return "fadou-mock-result:" + sessionId;
  }

  function getAttempt() {
    var key = attemptKey();
    var fromSession = sessionStorage.getItem(key);
    if (fromSession) return parseInt(fromSession, 10) || 1;
    var fromLocal = localStorage.getItem(key);
    if (fromLocal) return parseInt(fromLocal, 10) || 1;
    return 1;
  }

  function setAttempt(n) {
    sessionStorage.setItem(attemptKey(), String(n));
    localStorage.setItem(attemptKey(), String(n));
    currentAttempt = n;
  }

  function escapeHtml(text) {
    var div = document.createElement("div");
    div.textContent = text == null ? "" : String(text);
    return div.innerHTML;
  }

  function getSelectedValue(qid) {
    var el = formEl.querySelector('input[name="q' + qid + '"]:checked');
    return el ? el.value : null;
  }

  function optionText(q, letter) {
    if (!letter || !q.options) return "";
    return q.options[letter] || "";
  }

  function renderExam() {
    formEl.classList.remove("hidden");
    footerEl.classList.remove("hidden");
    resultsEl.classList.add("hidden");
    resultsEl.innerHTML = "";

    formEl.innerHTML = questions.map(function (q) {
      var opts = q.options || {};
      var keys = ["a", "b", "c", "d"];
      var optionsHtml = keys.map(function (k) {
        if (!opts[k]) return "";
        return (
          "<label>" +
          '<input type="radio" name="q' + q.id + '" value="' + k + '">' +
          "<span>(" + k + ") " + escapeHtml(opts[k]) + "</span>" +
          "</label>"
        );
      }).join("");

      return (
        '<article class="question-card" data-id="' + q.id + '">' +
        '<div class="question-meta">第 ' + q.id + " 題 · " + escapeHtml(q.category || "") +
        (q.section ? " / " + escapeHtml(q.section) : "") +
        (currentAttempt > 1 ? ' · <span class="attempt-tag">第 ' + currentAttempt + " 次測驗</span>" : "") +
        "</div>" +
        '<div class="question-stem">' + escapeHtml(q.stem || "") + "</div>" +
        '<div class="options">' + optionsHtml + "</div>" +
        "</article>"
      );
    }).join("");

    formEl.querySelectorAll('input[type="radio"]').forEach(function (input) {
      input.addEventListener("change", function () {
        saveDraft();
        updateProgress();
      });
    });
    updateProgress();
  }

  function countAnswered() {
    var n = 0;
    questions.forEach(function (q) {
      if (getSelectedValue(q.id)) n++;
    });
    return n;
  }

  function updateProgress() {
    var answered = countAnswered();
    var total = questions.length;
    var suffix = currentAttempt > 1 ? " · 第 " + currentAttempt + " 次測驗" : "";
    progressText.textContent = "已作答 " + answered + " / " + total + suffix;
    progressFill.style.width = total ? (answered / total * 100) + "%" : "0%";
  }

  function showRestoreToast() {
    var el = document.createElement("div");
    el.className = "restore-toast";
    el.textContent = "已恢復上次作答進度";
    headerEl.appendChild(el);
    setTimeout(function () {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 3000);
  }

  function saveDraft() {
    var answers = {};
    questions.forEach(function (q) {
      var v = getSelectedValue(q.id);
      if (v) answers[String(q.id)] = v;
    });
    try {
      localStorage.setItem(
        draftKey(),
        JSON.stringify({ answers: answers, savedAt: new Date().toISOString(), attempt: currentAttempt })
      );
    } catch (err) {
      console.warn("Could not save draft", err);
    }
  }

  function clearDraft() {
    try {
      localStorage.removeItem(draftKey());
    } catch (err) {
      /* ignore */
    }
  }

  function restoreDraft() {
    try {
      var raw = localStorage.getItem(draftKey());
      if (!raw) return;
      var data = JSON.parse(raw);
      if (data.attempt && data.attempt !== currentAttempt) return;
      var answers = data.answers || {};
      var restored = 0;
      Object.keys(answers).forEach(function (qid) {
        var input = formEl.querySelector('input[name="q' + qid + '"][value="' + answers[qid] + '"]');
        if (input) {
          input.checked = true;
          restored++;
        }
      });
      if (restored > 0) showRestoreToast();
      updateProgress();
    } catch (err) {
      console.warn("Could not restore draft", err);
    }
  }

  function getCategoryForId(id) {
    for (var i = 0; i < CATEGORY_RANGES.length; i++) {
      var r = CATEGORY_RANGES[i];
      if (id >= r.start && id <= r.end) return r.name;
    }
    return "其他";
  }

  function gradeExam() {
    var unanswered = [];
    var wrong = [];
    var correct = 0;
    var categoryStats = {};
    var reviewItems = [];

    CATEGORY_RANGES.forEach(function (r) {
      categoryStats[r.name] = { correct: 0, total: r.end - r.start + 1 };
    });

    questions.forEach(function (q) {
      var selected = getSelectedValue(q.id);
      var cat = getCategoryForId(q.id);
      if (!categoryStats[cat]) {
        categoryStats[cat] = { correct: 0, total: 0 };
      }
      categoryStats[cat].total++;

      var ans = (q.answer || "").toLowerCase();
      var status = "correct";

      if (!selected) {
        unanswered.push(q.id);
        status = "unanswered";
      } else if (selected === ans) {
        correct++;
        categoryStats[cat].correct++;
      } else {
        wrong.push(q.id);
        status = "wrong";
      }

      if (status !== "correct") {
        reviewItems.push({
          id: q.id,
          status: status,
          category: q.category || cat,
          section: q.section || "",
          stem: q.stem || "",
          options: q.options || {},
          selected: selected,
          selectedText: selected ? optionText(q, selected) : "",
          correct: ans,
          correctText: optionText(q, ans)
        });
      }
    });

    var score = correct * 2;
    var passed = score >= passScore;

    return {
      score: score,
      passed: passed,
      correct: correct,
      wrong: wrong,
      unanswered: unanswered,
      categoryStats: categoryStats,
      reviewItems: reviewItems,
      attempt: currentAttempt
    };
  }

  function buildReviewMarkdown(result) {
    var lines = [
      "# 法鬥超人模擬考 · 錯題檢討",
      "得分：" + result.score + "/100 · 第 " + result.attempt + " 次測驗 · " + new Date().toLocaleString("zh-TW")
    ];
    if (!result.reviewItems.length) {
      lines.push("", "本次無錯題或未作答，做得好！");
      return lines.join("\n");
    }
    result.reviewItems.forEach(function (item) {
      var label = item.status === "unanswered" ? "未作答" : "答錯";
      lines.push("");
      lines.push("## 第 " + item.id + " 題（" + item.category + "）· " + label);
      lines.push("題幹：" + item.stem);
      ["a", "b", "c", "d"].forEach(function (k) {
        if (item.options[k]) lines.push("(" + k + ") " + item.options[k]);
      });
      lines.push(
        "你的答案：" + (item.selected ? "(" + item.selected + ") " + item.selectedText : "（未作答）")
      );
      lines.push("正解：(" + item.correct + ") " + item.correctText);
    });
    lines.push("", "請法鬥超人解析錯題原因。");
    return lines.join("\n");
  }

  function buildReviewHtml(result) {
    if (!result.reviewItems.length) {
      return '<p class="review-empty">本次無錯題或未作答，做得好！</p>';
    }
    return (
      '<div class="review-section">' +
      "<h3>錯題檢討</h3>" +
      result.reviewItems.map(function (item) {
        var label = item.status === "unanswered" ? "未作答" : "答錯";
        var optsHtml = ["a", "b", "c", "d"].map(function (k) {
          if (!item.options[k]) return "";
          return "<li>(" + k + ") " + escapeHtml(item.options[k]) + "</li>";
        }).join("");
        return (
          '<article class="review-card review-' + item.status + '">' +
          '<div class="review-meta">第 ' + item.id + " 題 · " + escapeHtml(item.category) +
          (item.section ? " / " + escapeHtml(item.section) : "") +
          ' · <span class="review-tag">' + label + "</span></div>" +
          '<p class="review-stem">' + escapeHtml(item.stem) + "</p>" +
          '<ul class="review-options">' + optsHtml + "</ul>" +
          '<p class="review-your"><strong>你的答案：</strong>' +
          (item.selected
            ? "(" + item.selected + ") " + escapeHtml(item.selectedText)
            : "（未作答）") +
          "</p>" +
          '<p class="review-correct"><strong>正解：</strong>(' + item.correct + ") " +
          escapeHtml(item.correctText) + "</p>" +
          "</article>"
        );
      }).join("") +
      "</div>"
    );
  }

  function saveResultSession(result, reviewMarkdown) {
    try {
      sessionStorage.setItem(
        resultKey(),
        JSON.stringify({ attempt: currentAttempt, result: result, reviewMarkdown: reviewMarkdown })
      );
    } catch (err) {
      console.warn("Could not save result session", err);
    }
  }

  function clearResultSession() {
    try {
      sessionStorage.removeItem(resultKey());
    } catch (err) {
      /* ignore */
    }
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        alert("已複製到剪貼簿！");
      });
    } else {
      prompt("請複製以下內容：", text);
    }
  }

  function downloadReview(markdown) {
    var name = "錯題檢討-" + sessionId + "-第" + currentAttempt + "次.md";
    var blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function showResults(result, reviewMarkdown, fromRestore) {
    formEl.classList.add("hidden");
    footerEl.classList.add("hidden");

    if (!fromRestore) {
      clearDraft();
      saveResultSession(result, reviewMarkdown);
    }

    var statusText = result.passed ? "恭喜及格！" : "尚未及格，繼續加油！";
    var statusClass = result.passed ? "pass" : "fail";

    var catHtml = CATEGORY_RANGES.map(function (r) {
      var s = result.categoryStats[r.name] || { correct: 0, total: 0 };
      return "<li>" + escapeHtml(r.name) + "：" + s.correct + " / " + s.total + " 題正確（" + (s.correct * 2) + " 分）</li>";
    }).join("");

    var wrongText = result.wrong.length ? result.wrong.join("、") : "無";
    var unansText = result.unanswered.length
      ? "（未作答：" + result.unanswered.join("、") + "）"
      : "";

    resultsEl.innerHTML =
      '<div class="score-box ' + statusClass + '">' +
      "<h2>交卷結果</h2>" +
      (result.attempt > 1 ? '<p class="attempt-line">第 ' + result.attempt + " 次測驗</p>" : "") +
      '<p class="score-value">' + result.score + " / 100</p>" +
      "<p>" + statusText + "（及格線 " + passScore + " 分）</p>" +
      "<p>答對 " + result.correct + " 題，答錯 " + result.wrong.length + " 題" + unansText + "</p>" +
      '<ul class="category-scores">' + catHtml + "</ul>" +
      '<div class="wrong-list"><strong>錯題題號：</strong>' + wrongText + "</div>" +
      buildReviewHtml(result) +
      '<div class="result-actions">' +
      '<button type="button" class="btn-secondary" id="copy-review">複製錯題檢討（貼回 Cursor）</button>' +
      '<button type="button" class="btn-secondary" id="download-review">下載錯題檢討.md</button>' +
      '<button type="button" class="btn-primary" id="retest-btn">重新測試</button>' +
      "</div>" +
      '<p class="result-hint">關閉分頁再開啟會從空白卷開始；按 F5 仍保留本次成績。</p>' +
      "</div>";

    resultsEl.classList.remove("hidden");

    document.getElementById("copy-review").addEventListener("click", function () {
      copyText(reviewMarkdown);
    });
    document.getElementById("download-review").addEventListener("click", function () {
      downloadReview(reviewMarkdown);
    });
    document.getElementById("retest-btn").addEventListener("click", function () {
      if (!confirm("確定要重新測試？將開始新一輪作答（同一套 50 題）。")) return;
      clearResultSession();
      setAttempt(currentAttempt + 1);
      renderExam();
      restoreDraft();
      window.scrollTo(0, 0);
    });
  }

  function tryRestoreSubmitted() {
    try {
      var raw = sessionStorage.getItem(resultKey());
      if (!raw) return false;
      var payload = JSON.parse(raw);
      if (payload.attempt !== currentAttempt) return false;
      showResults(payload.result, payload.reviewMarkdown, true);
      return true;
    } catch (err) {
      return false;
    }
  }

  submitBtn.addEventListener("click", function () {
    var unanswered = questions.length - countAnswered();
    if (unanswered > 0) {
      var ok = confirm("還有 " + unanswered + " 題未作答，確定要交卷嗎？");
      if (!ok) return;
    }
    var result = gradeExam();
    showResults(result, buildReviewMarkdown(result), false);
    window.scrollTo(0, 0);
  });

  if (questions.length !== 50) {
    console.warn("Expected 50 questions, got " + questions.length);
  }

  if (!tryRestoreSubmitted()) {
    renderExam();
    restoreDraft();
  }
})();

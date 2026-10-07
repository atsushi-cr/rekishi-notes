/* 歴史学 共通スクリプト：テーマ切替・目次生成・トップへ戻る */
(function () {
  var root = document.documentElement;

  function load(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function save(key, val) { try { localStorage.setItem(key, val); } catch (e) {} }

  // 保存済みテーマを反映（未設定なら端末の設定に従う）
  var saved = load("rekishi-theme");
  if (saved) root.setAttribute("data-theme", saved);

  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  document.addEventListener("DOMContentLoaded", function () {
    // テーマ切替ボタン
    var btn = document.querySelector(".theme-toggle");
    if (btn) {
      var paint = function () {
        btn.textContent = isDark() ? "☀" : "☾";
        btn.setAttribute("aria-label", isDark() ? "明るい表示にする" : "暗い表示にする");
      };
      paint();
      btn.addEventListener("click", function () {
        var next = isDark() ? "light" : "dark";
        root.setAttribute("data-theme", next);
        save("rekishi-theme", next);
        paint();
      });
    }

    // 目次：main 内の h2[id] から自動生成
    var toc = document.querySelector(".toc ol");
    if (toc) {
      document.querySelectorAll("main h2[id]").forEach(function (h) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent;
        li.appendChild(a);
        toc.appendChild(li);
      });
    }

    // トップへ戻るボタン
    var top = document.createElement("button");
    top.className = "to-top";
    top.type = "button";
    top.textContent = "↑";
    top.setAttribute("aria-label", "ページの先頭へ");
    top.addEventListener("click", function () { window.scrollTo({ top: 0 }); });
    document.body.appendChild(top);
    window.addEventListener("scroll", function () {
      top.classList.toggle("show", window.scrollY > 600);
    }, { passive: true });
  });
})();

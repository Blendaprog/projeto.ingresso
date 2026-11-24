(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const form = $("demoPaymentForm");
  const payButton = $("payButton");
  const status = $("paymentStatus");
  const overlay = $("processingOverlay");

  function setStatus(message, error = false) {
    if (!status) return;
    status.classList.toggle("is-error", error);
    const text = status.querySelector("span:last-child");
    if (text) text.textContent = message;
  }

  // Cartão ilustrativo: os campos não têm atributo name e nunca são enviados.
  const cardName = $("cardName");
  const cardNumber = $("cardNumber");
  const cardExpiry = $("cardExpiry");
  const previewName = $("previewName");
  const previewNumber = $("previewNumber");
  const previewExpiry = $("previewExpiry");
  const cardPreview = $("cardPreview");

  if (cardName) {
    cardName.addEventListener("input", () => {
      previewName.textContent = cardName.value.trim().toUpperCase() || "SEU NOME";
    });
    cardNumber.addEventListener("input", () => {
      const digits = cardNumber.value.replace(/\D/g, "").slice(0, 16);
      cardNumber.value = digits.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
      previewNumber.textContent = digits
        ? (digits + "••••••••••••••••").slice(0, 16).replace(/(.{4})/g, "$1 ").trim()
        : "•••• •••• •••• ••••";
    });
    cardExpiry.addEventListener("input", () => {
      const digits = cardExpiry.value.replace(/\D/g, "").slice(0, 4);
      cardExpiry.value = digits.length > 2 ? digits.slice(0, 2) + "/" + digits.slice(2) : digits;
      previewExpiry.textContent = cardExpiry.value || "MM/AA";
    });
    [cardName, cardNumber, cardExpiry].forEach((field) => {
      field.addEventListener("focus", () => cardPreview.classList.add("is-focused"));
      field.addEventListener("blur", () => cardPreview.classList.remove("is-focused"));
    });
  }

  // QR decorativo gerado localmente. Não contém dados de cobrança PIX.
  const qr = $("demoQr");
  if (qr) {
    const seed = "TICKETSHOW-DEMO-NAO-PAGAVEL";
    const size = 21;
    const finder = (x, y, ox, oy) => {
      const dx = x - ox, dy = y - oy;
      if (dx < 0 || dy < 0 || dx > 6 || dy > 6) return null;
      return dx === 0 || dy === 0 || dx === 6 || dy === 6 ||
        (dx >= 2 && dx <= 4 && dy >= 2 && dy <= 4);
    };
    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        let dark = null;
        for (const [ox, oy] of [[0,0],[14,0],[0,14]]) {
          const mark = finder(x, y, ox, oy);
          if (mark !== null) dark = mark;
        }
        if (dark === null) dark = ((x * 7 + y * 11 + seed.charCodeAt((x + y) % seed.length)) % 5) < 2;
        const cell = document.createElement("i");
        cell.className = "ts-qr-cell" + (dark ? " is-dark" : "");
        qr.appendChild(cell);
      }
    }
  }

  // Contador apenas visual, sem validade de cobrança.
  const timer = $("pixTimer");
  if (timer) {
    let seconds = 300;
    window.setInterval(() => {
      if (seconds > 0) seconds -= 1;
      timer.textContent = String(Math.floor(seconds / 60)).padStart(2, "0") + ":" +
        String(seconds % 60).padStart(2, "0");
    }, 1000);
  }

  const copyButton = $("copyPix");
  if (copyButton) {
    copyButton.addEventListener("click", async () => {
      const code = $("fakePixCode").textContent;
      try {
        await navigator.clipboard.writeText(code);
        copyButton.textContent = "Copiado ✓";
      } catch (_) {
        const helper = document.createElement("textarea");
        helper.value = code;
        document.body.appendChild(helper);
        helper.select();
        try { document.execCommand("copy"); copyButton.textContent = "Copiado ✓"; }
        catch (_) { copyButton.textContent = "Código de exemplo"; }
        helper.remove();
      }
      window.setTimeout(() => { copyButton.textContent = "Copiar"; }, 1800);
    });
  }

  if (form && payButton) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (cardName) {
        const digits = cardNumber.value.replace(/\D/g, "");
        const expiry = cardExpiry.value;
        const validExpiry = /^\d{2}\/\d{2}$/.test(expiry) &&
          Number(expiry.slice(0, 2)) >= 1 && Number(expiry.slice(0, 2)) <= 12;
        if (cardName.value.trim().length < 2) {
          setStatus("Digite um nome fictício para visualizar o cartão.", true);
          cardName.focus();
          return;
        }
        if (digits.length < 12) {
          setStatus("Digite pelo menos 12 números fictícios para a prévia.", true);
          cardNumber.focus();
          return;
        }
        if (!validExpiry) {
          setStatus("Informe uma validade fictícia no formato MM/AA.", true);
          cardExpiry.focus();
          return;
        }
      }
      payButton.disabled = true;
      payButton.querySelector("span").textContent = "Finalizando demonstração...";
      setStatus("Tudo certo! A demonstração está sendo finalizada.");
      if (overlay) {
        overlay.classList.add("is-visible");
        overlay.setAttribute("aria-hidden", "false");
      }
      window.setTimeout(() => form.submit(), 1150);
    });
  }
})();
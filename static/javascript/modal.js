const locale_modal = document.getElementById("locale-modal");
const locale_btn = document.getElementById("locale-btn");
const eng_btn = document.getElementById("eng-btn");
const kor_btn = document.getElementById("kor-btn");
const locale_close = document.getElementById("locale-close");
const currency_modal = document.getElementById("currency-modal");
const currency_btn = document.getElementById("currency-btn");
const usd_btn = document.getElementById("usd-btn");
const krw_btn = document.getElementById("krw-btn");
const currency_close = document.getElementById("currency-close");
locale_btn.onclick = () => {
  locale_modal.style.display = "block";
};
locale_close.onclick = () => {
  locale_modal.style.display = "";
};
eng_btn.onclick = () => {
  fetch(`${lang_url}?lang=en`).then(() => window.location.reload());
};
kor_btn.onclick = () => {
  fetch(`${lang_url}?lang=ko`).then(() => window.location.reload());
};
currency_btn.onclick = () => {
  currency_modal.style.display = "block";
};
currency_close.onclick = () => {
  currency_modal.style.display = "";
};
usd_btn.onclick = () => {
  fetch(`${currency_url}?currency=en`).then(() => window.location.reload());
};
krw_btn.onclick = () => {
  fetch(`${currency_url}?currency=ko`).then(() => window.location.reload());
};
window.onclick = (e) => {
  if (e.target == locale_modal) {
    locale_modal.style.display = "";
  } else if (e.target == currency_modal) {
    currency_modal.style.display = "";
  }
};

"use strict";
(() => {
  // Original lightweight SVG scene art: no external assets, font downloads or
  // per-user network calls. Fixed illustrated Greek town and scene props.
  const backgrounds={
    meet:`<rect x="0" y="0" width="800" height="320" fill="url(#sky)"/><circle cx="665" cy="58" r="37" fill="#ffe3a3" opacity=".92"/><path d="M0 185Q180 123 320 186T800 179V320H0" fill="#bfd9c0"/><path d="M0 215Q200 187 400 214T800 200V320H0" fill="#8dbdb2"/>`,
    transport:`<rect width="800" height="320" fill="url(#sky)"/><circle cx="680" cy="55" r="39" fill="#ffdc9b"/><path d="M0 206Q140 164 310 206T800 201V320H0" fill="#bad6c5"/>`,
    market:`<rect width="800" height="320" fill="url(#sky)"/><circle cx="680" cy="58" r="36" fill="#ffdda1"/><path d="M0 219Q170 181 370 205T800 212V320H0" fill="#c9d9bc"/>`,
    home:`<rect width="800" height="320" fill="url(#sky)"/><circle cx="679" cy="54" r="35" fill="#ffdda1"/><path d="M0 215Q140 174 310 202T800 208V320H0" fill="#a0c6ac"/>`,
    park:`<rect width="800" height="320" fill="url(#sky)"/><circle cx="670" cy="60" r="36" fill="#ffdda1"/><path d="M0 193Q200 148 372 184T800 185V320H0" fill="#b4d3a5"/><path d="M0 244Q200 203 410 238T800 232V320H0" fill="#7fb395"/>`
  };
  const common=`<path d="M0 275H800V320H0Z" fill="#e8d3b2"/><path d="M0 276H800" stroke="#d0af88" stroke-width="6"/>
    <g opacity=".7"><path d="M40 291H146M225 299H340M455 291H570M670 301H755" stroke="#cfae84" stroke-width="2" stroke-linecap="round"/></g>
    <g transform="translate(94 171)"><rect x="0" y="17" width="14" height="105" rx="7" fill="#81635b"/><circle cx="6" cy="12" r="36" fill="#6caa89"/><circle cx="-17" cy="35" r="28" fill="#609d82"/><circle cx="23" cy="34" r="31" fill="#88b78c"/></g>`;
  const person=(x,y,shirt,hair="#3b4154")=>`<g transform="translate(${x} ${y})">
    <ellipse cx="0" cy="104" rx="30" ry="7" fill="#61747b" opacity=".2"/>
    <path d="M-12 60L-18 101M12 60L17 101" stroke="#30455d" stroke-width="13" stroke-linecap="round"/>
    <path d="M-22 35Q0 27 22 35L18 71H-19Z" fill="${shirt}"/>
    <path d="M-23 39L-37 69M23 39L35 67" stroke="${shirt}" stroke-width="11" stroke-linecap="round"/>
    <circle cx="0" cy="13" r="21" fill="#e9b28c"/>
    <path d="M-20 12Q-25-15-7-19Q15-30 22-1L20 12Q15-11-4-7Z" fill="${hair}"/>
    <circle cx="-7" cy="13" r="1.7" fill="#44414b"/><circle cx="8" cy="13" r="1.7" fill="#44414b"/>
    <path d="M-5 23Q0 27 6 23" fill="none" stroke="#a6695d" stroke-width="1.8" stroke-linecap="round"/>
  </g>`;
  const houses=`<g transform="translate(286 70)">
    <rect x="0" y="20" width="210" height="190" rx="9" fill="#f6e7cc"/>
    <path d="M-18 35L103-21L230 35Z" fill="#d98973"/>
    <rect x="22" y="60" width="52" height="64" rx="18" fill="#7dadd1"/>
    <rect x="137" y="60" width="52" height="64" rx="18" fill="#7dadd1"/>
    <path d="M48 61V123M162 61V123" stroke="#fff4d8" stroke-width="5"/>
    <path d="M84 210V121Q106 91 128 121V210Z" fill="#497e83"/>
    <circle cx="117" cy="159" r="3" fill="#ffcf88"/>
    <path d="M20 45H194" stroke="#e0b58e" stroke-width="3"/>
  </g>`;
  const bus=`<g transform="translate(275 130)">
    <ellipse cx="160" cy="151" rx="179" ry="15" fill="#344d58" opacity=".15"/>
    <rect x="0" y="15" width="350" height="128" rx="27" fill="#f3c76c"/>
    <rect x="8" y="23" width="333" height="72" rx="15" fill="#5f9bb5"/>
    <path d="M94 24V96M187 24V96M285 24V140" stroke="#f7dca3" stroke-width="8"/>
    <rect x="11" y="103" width="329" height="21" fill="#dfab5b"/>
    <rect x="110" y="29" width="76" height="29" rx="7" fill="#183b55"/>
    <text x="147" y="49" text-anchor="middle" fill="#f1e5b9" font-size="19" font-family="sans-serif">55</text>
    <circle cx="83" cy="141" r="29" fill="#34455a"/><circle cx="83" cy="141" r="14" fill="#acc7cf"/>
    <circle cx="285" cy="141" r="29" fill="#34455a"/><circle cx="285" cy="141" r="14" fill="#acc7cf"/>
    <rect x="320" y="106" width="22" height="10" rx="3" fill="#ffecca"/>
  </g>`;
  const shop=`<g transform="translate(276 49)">
    <rect x="0" y="31" width="277" height="197" rx="9" fill="#f2e0be"/>
    <rect x="0" y="31" width="277" height="39" rx="8" fill="#598c92"/>
    <text x="138" y="58" text-anchor="middle" fill="#fff6df" font-size="20" letter-spacing="2" font-weight="bold" font-family="sans-serif">ΠΕΡΙΠΤΕΡΟ</text>
    <path d="M0 71H277L264 109H10Z" fill="#e6a46c"/>
    <path d="M13 71H55L53 104H5ZM102 71H144L144 104H93ZM188 71H229L234 104H181Z" fill="#fff0d0"/>
    <rect x="27" y="117" width="222" height="87" rx="6" fill="#91bbbd"/>
    <rect x="33" y="162" width="207" height="6" rx="3" fill="#668d91"/>
    <g fill="#e0ba79"><circle cx="68" cy="147" r="15"/><circle cx="101" cy="146" r="13"/></g>
    <g fill="#d86e66"><circle cx="156" cy="150" r="13"/><circle cx="183" cy="149" r="11"/></g>
    <rect x="26" y="200" width="224" height="21" rx="3" fill="#b46c5a"/>
  </g>`;
  const cafe=`<g transform="translate(325 55)">
    <rect x="0" y="21" width="226" height="211" rx="10" fill="#f4e0c1"/>
    <path d="M-7 72H230V97H-7Z" fill="#c9776d"/>
    <path d="M3 72H44V96H3ZM84 72H126V96H84ZM170 72H211V96H170Z" fill="#fff2d4"/>
    <rect x="34" y="106" width="62" height="77" rx="19" fill="#7aaec3"/>
    <rect x="132" y="106" width="62" height="77" rx="19" fill="#7aaec3"/>
    <path d="M66 110V179M163 110V179" stroke="#fff0cc" stroke-width="5"/>
    <text x="113" y="55" text-anchor="middle" fill="#774e4b" font-size="18" font-family="sans-serif" font-weight="bold">ΚΑΦΕ</text>
  </g><g transform="translate(570 232)"><path d="M-48 0H50M0-30V30" stroke="#6b6357" stroke-width="7" stroke-linecap="round"/>
    <ellipse cx="0" cy="-32" rx="65" ry="10" fill="#e6c193"/>
    <rect x="-19" y="-62" width="35" height="26" rx="7" fill="#fff8e7"/>
    <path d="M16-56Q37-60 30-43Q25-36 16-42" stroke="#fff8e7" stroke-width="6" fill="none"/>
  </g>`;
  const park=`<g transform="translate(370 137)"><path d="M-7 69V131M77 69V131" stroke="#634d4e" stroke-width="9"/>
    <path d="M-33 71H100M-26 89H94M-20 107H90" stroke="#b87b59" stroke-width="12" stroke-linecap="round"/>
    <path d="M-30 72L-30 98M98 72L98 98" stroke="#634d4e" stroke-width="7"/></g>
    <g transform="translate(619 121)"><rect x="-6" y="35" width="13" height="135" rx="7" fill="#73594e"/>
    <circle cx="-5" cy="27" r="65" fill="#6baf84"/><circle cx="-45" cy="46" r="43" fill="#5aa27f"/>
    <circle cx="31" cy="49" r="44" fill="#8abb8f"/></g>`;
  const idToKind={
    meet:"meet",home_city:"home",family:"home",languages:"meet",
    ticket:"transport",daily:"home",groceries:"market",clothes:"market",
    directions:"home",cafe:"cafe",plans:"park",
    route:"transport",periptero:"market",likes:"park"
  };
  function illustration(id){
    const kind=idToKind[id]||"meet";
    const svgNS="http://www.w3.org/2000/svg";
    const svg=document.createElementNS(svgNS,"svg");
    svg.setAttribute("viewBox","0 0 800 320");
    svg.setAttribute("role","img");
    svg.setAttribute("aria-label","Illustrated Greek town scene");
    const foreground=kind==="transport"?bus:kind==="market"?shop:
      kind==="cafe"?cafe:kind==="park"?park:houses;
    const people=kind==="transport"?person(170,197,"#db8d71"):
      kind==="market"?person(624,196,"#5c92b5"):
      kind==="cafe"?person(246,193,"#6887a1"):
      kind==="park"?person(255,189,"#d78d75"):
      person(192,190,"#d58f7d")+person(638,194,"#718cac");
    svg.innerHTML=`<defs><linearGradient id="lexi-life-sky" x1="0" y1="0" x2="0" y2="1">
      <stop stop-color="#83bed5"/><stop offset="1" stop-color="#f6e3ba"/></linearGradient>
      <linearGradient id="sky"><stop stop-color="#8cc3d0"/><stop offset="1" stop-color="#f4dfbc"/></linearGradient></defs>
      ${backgrounds[kind]}${common}${foreground}${people}
      <g fill="#ffffff" opacity=".6"><ellipse cx="75" cy="65" rx="45" ry="13"/><ellipse cx="112" cy="65" rx="35" ry="16"/></g>`;
    return svg;
  }
  window.LexiScenes={illustration};
})();

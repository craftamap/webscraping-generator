import "fontsource-dancing-script/index.css";
import "fontsource-lato/index.css";
import "./index.scss";
import Template from "./index.hbs";
import $ from "jquery";


setTimeout(() => {
    $(".spinner").fadeOut(500, () => {
        $(".spinner").remove()
        $(".root").html(Template({flag: "OLA-WEBSCRAPING-2grNexpBnz"}));
        $(".content").fadeIn(500)
    })
}, 2000);

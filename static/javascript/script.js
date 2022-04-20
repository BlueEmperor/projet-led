$(document).ready(function () {
  function t() {
    for (let i = 0; i < $(".btn-script").length; i++) {
      if($("#script-"+(i+1)).css("background-color") != "rgb(255, 255, 255)") {
        $("#script-"+(i+1)).removeClass().addClass("btn-script non-select");
      }
    }
  }

  class ColorPicker {
    constructor(root) {
      this.root = root;
      this.colorjoe = colorjoe.rgb(this.root.querySelector(".colorjoe"));
      this.selectedColor = null;
      this.savedColors = this.getSavedColors();

      this.colorjoe.show();
      this.setSelectedColor("#000000");
      this.colorjoe.on("change", (color) => {
        this.setSelectedColor(color.hex(), true);
        $.ajax({
          url: "../color?color=" + color.hex().substr(1, 6),
          method: "GET",
        });
        t()
      });
    }

    setSelectedColor(color, skipCjUpdate = false) {
      this.selectedColor = color;
      this.root.querySelector(".selected-color").style.background = color;
    }

    getSavedColors() {
      return ["#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff"];
    }
  }
  const cp = new ColorPicker(document.querySelector(".container-colorjoe"));

  // Switch state button
  $("#switch").on("click", function (e) {
    let status;

    if ($(this).css("background-color") == "rgb(76, 175, 80)") {
      $(this).removeClass().addClass("btn off");
      $("#lock").removeClass().addClass("btn off");
      status = "off";
    } else if ($(this).css("background-color") == "rgb(244, 67, 54)") {
      $(this).removeClass().addClass("btn on");
      status = "on";
    }

    $.ajax({
      url: "../switch?status=" + status,
      method: "GET",
    });
  });

  $("#lock").on("click", function (e) {
    let status;

    if ($(this).css("background-color") == "rgb(76, 175, 80)") {
      $(this).removeClass().addClass("btn off");
      status = "off";
    } else if ($(this).css("background-color") == "rgb(244, 67, 54)") {
      $(this).removeClass().addClass("btn on");
      status = "on";
    }

    $.ajax({
      url: "../lock?status=" + status,
      method: "GET",
    });
  });
  $(".btn-script").on("click", function (e) {
    
    let script;
    
    if ($(this).css("background-color") == "rgb(255, 255, 255)") {
      t()
      $(this).removeClass().addClass("btn-script select");
      script = $(this).text();
    } else if ($(this).css("background-color") == "rgb(76, 175, 80)") {
      t()
      $(this).removeClass().addClass("btn-script non-select");
      script="stop";
    }

    $.ajax({
      url: "../script?script=" + script,
      method: "GET",
    });
  });
});
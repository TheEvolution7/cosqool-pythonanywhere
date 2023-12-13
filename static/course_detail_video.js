const editorElements = document.querySelectorAll(".editor");
editorElements.forEach((editorElement) => {
  ClassicEditor.create(editorElement, {})
    .then((editor) => {})

    .catch((error) => {
      console.error(error);
    });
});

var create_playlist_modal = new bootstrap.Modal(
  document.getElementById("create-playlist-modal"),
  {}
);

const add_playlist_form = document.getElementById("add_playlist_form");
add_playlist_form.addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData(add_playlist_form);

  const formDataJSON = {};
  formData.forEach((value, key) => {
    formDataJSON[key] = value;
  });

  const request = new Request(add_playlist_form.getAttribute("action"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(formDataJSON),
  });
  fetch(request)
    .then(function (response) {
      if (response.ok) {
        return response.text();
      } else {
        throw new Error("Network response was not ok");
      }
    })
    .then(function (data) {
      Swal.fire("Successfully!", "success");
      add_playlist_form.reset();
      create_playlist_modal.hide();
    })
    .catch(function (error) {
      console.error("There was a problem with the fetch operation:", error);
      Swal.fire(
        "Error!",
        "An error occurred while processing your request.",
        "error"
      );
    });
});

const add_note_form = document.getElementById("add_note_form");
add_note_form.addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData(add_note_form);

  const formDataJSON = {};
  formData.forEach((value, key) => {
    formDataJSON[key] = value;
  });

  const request = new Request(add_note_form.getAttribute("action"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(formDataJSON),
  });
  fetch(request)
    .then(function (response) {
      if (response.ok) {
        return response.text();
      } else {
        throw new Error("Network response was not ok");
      }
    })
    .then(function (data) {
      Swal.fire("Successfully!", "success");
      add_note_form.reset();
    })
    .catch(function (error) {
      console.error("There was a problem with the fetch operation:", error);
      Swal.fire(
        "Error!",
        "An error occurred while processing your request.",
        "error"
      );
    });
});

const update_note_forms = document.querySelectorAll(".update_note_form");
update_note_forms.forEach((update_note_form) => {
  update_note_form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(update_note_form);

    const formDataJSON = {};
    formData.forEach((value, key) => {
      formDataJSON[key] = value;
    });

    const request = new Request(update_note_form.getAttribute("action"), {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(formDataJSON),
    });
    fetch(request).then(function (response) {
      Swal.fire("Successfully!", "", "success");
    });
  });
});

const delete_note_btns = document.querySelectorAll(".delete_note_btn");
delete_note_btns.forEach((delete_note_btn) => {
  delete_note_btn.addEventListener("click", (e) => {
    e.preventDefault();

    const request = new Request(delete_note_btn.getAttribute("delete-url"), {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    });
    fetch(request).then(function (response) {
      if (response.status == "404") {
        Swal.fire("Error!", "", "error");
      } else {
        $("#note-" + delete_note_btn.getAttribute("btn-id")).hide();
        Swal.fire("Successfully!", "", "success");
      }
    });
  });
});

const video_update_playlist_forms = document.querySelectorAll(
  ".video_update_playlist_form"
);
video_update_playlist_forms.forEach((video_update_playlist_form) => {
  video_update_playlist_form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(video_update_playlist_form);

    const formDataJSON = {};
    formData.forEach((value, key) => {
      formDataJSON[key] = value;
    });

    const request = new Request(
      video_update_playlist_form.getAttribute("action"),
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(formDataJSON),
      }
    );
    fetch(request).then(function (response) {
      Swal.fire("Successfully!", "", "success");
    });
  });
});

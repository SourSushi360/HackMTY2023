const projectName = 'survey-form';
localStorage.setItem('example_project', 'Survey Form');

const textFields = document.querySelectorAll('.mdc-text-field');
for (const textField of textFields) {
  mdc.textField.MDCTextField.attachTo(textField);
}

mdc.select.MDCSelect.attachTo(document.querySelector('.mdc-select'));

var radios = document.querySelectorAll('.mdc-radio');
for (var i = 0, radio; radio = radios[i]; i++) {
  new mdc.radio.MDCRadio(radio);
}
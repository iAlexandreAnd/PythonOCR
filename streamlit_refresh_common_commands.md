# Streamlit actions that commonly trigger script reruns

- Selecting, replacing, or removing a file with `st.file_uploader`
- Clicking `st.button`
- Checking or unchecking `st.checkbox`
- Choosing an option with `st.radio`, `st.selectbox`, or `st.pills`
- Choosing or clearing values in `st.multiselect`
- Moving a `st.slider` or adjusting `st.select_slider`
- Entering or changing text in `st.text_input` or `st.text_area`
- Selecting a date/time with `st.date_input` or `st.time_input`
- Changing a number in `st.number_input`
- Uploading or changing a file with `st.camera_input`
- Interacting with `st.data_editor`
- Submitting `st.form`; widgets inside a form submit together instead of rerunning on every change
- Using navigation methods such as `st.switch_page`
- Clicking links or controls that trigger a fragment rerun or another Streamlit UI action
- Receiving a change from session-state callbacks or widget `on_change` handlers

## Widget callbacks

Some widgets support callbacks. The callback runs first, and then Streamlit reruns the script:

```python
def on_change():
    st.write("This runs before the script reruns")

st.text_input("Name", on_change=on_change)
```

Not every UI event reruns the complete script immediately. Widgets inside `st.form` wait until `st.form_submit_button` is clicked, and `st.fragment` reruns only the fragment rather than the entire script.

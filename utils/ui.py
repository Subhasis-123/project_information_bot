from pathlib import Path

import streamlit as st


class UIService:

    def load_css(self):

        css_path = Path(

            "styles/style.css"

        )

        with open(

            css_path,

            encoding="utf-8"

        ) as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True

            )

    # ==============================

    def title(

        self,

        title,

        subtitle

    ):

        st.markdown(

            f"""

<div class="main-title">

{title}

</div>

<div class="sub-title">

{subtitle}

</div>

""",

            unsafe_allow_html=True

        )


ui = UIService()
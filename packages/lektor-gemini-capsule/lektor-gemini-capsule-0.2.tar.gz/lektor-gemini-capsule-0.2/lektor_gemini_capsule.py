# -*- coding: utf-8 -*-
from lektor.build_programs import BuildProgram
from lektor.db import Record
from lektor.pluginsystem import Plugin
from lektor.sourceobj import VirtualSourceObject
from lektor.utils import build_url

class GeminiSource(VirtualSourceObject):
    @property
    def path(self):
        return f'{self.record.path}@gemini'

    @property
    def source_content(self):
        with open(self.record.source_filename) as f:
            return f.read().decode("utf-8")

    @property
    def url_path(self):
        return build_url([self.record.url_path, "index.gmi"])

    def iter_source_filenames(self):
        return self.record.iter_source_filenames()


class GeminiBuildProgram(BuildProgram):
    # Based on:
    # https://www.getlektor.com/docs/api/environment/add-build-program/
    def produce_artifacts(self):
        self.declare_artifact(
            self.source.url_path, sources=list(self.source.iter_source_filenames())
        )

    def build_artifact(self, artifact):
        # Emulate the requirement and use of 'templates/MODEL.gmi' behaviour
        # This makes for a mostly seamless port of a website to a Gemini capsule
        artifact.render_template_into(
            f'{self.source.record["_model"]}.gmi', this=self.source.record
        )


class GeminiCapsulePlugin(Plugin):
    name = "gemini-capsule"
    description = "Simple plugin to produce Gemini capsules with lektor."

    def on_setup_env(self, **extra):
        # Register the BuildProgram
        self.env.add_build_program(GeminiSource, GeminiBuildProgram)

        @self.env.generator
        def generate_source_file(node):
            if isinstance(node, Record) and not node.is_attachment:
                # Allow skipping gemini generation with a special field
                if not ("_skip_gemini" in node and node["_skip_gemini"]):
                    yield GeminiSource(node)

        @self.env.virtualpathresolver("gemini")
        def resolve_virtual_path(record, pieces):
            if not pieces:
                return GeminiSource(record)

        @self.env.urlresolver
        def match_source_file(node, url_path):
            if url_path == [ "index.gmi" ] \
                    and isinstance(node, Record) \
                    and not node.is_attachment:
                        return GeminiSource(node)

        try:
            # This doesn't work currently due to lektor requiring 
            #   mistune < 2 and md2gemini requiring mistune >= 2
            # Hopefully either of these will be solved soon.
            from md2gemini import md2gemini as _md2gemini
        except ImportError:
            print('Could not import md2gemini, using raw markdown')
            def _md2gemini(data, **kwords):
                # Fallback to a pass-through function
                return data

        def md2gemini_filter(data, **kwords):
            # Change the default behaviour for links to something friendlier
            if 'links' not in kwords:
                kwords['links'] = 'paragraph'
            return _md2gemini(data, **kwords)

        self.env.jinja_env.filters['md2gemini'] = md2gemini_filter

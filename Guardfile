# Execute `guard` server to watch for file changes to trigger
# automatic coffeescript compilation.

guard 'coffeescript', :output => 'assets' do
  watch(/^src\/(.*).coffee/)
end

guard 'livereload', :apply_js_live => false do
  watch(/^.+\.html$/)
  watch(/^.+\.css$/)
  watch(/^.+\.js$/)
end

guard 'compass', :configuration_file => 'compass.config.rb' do
  watch(/^.+\/(.*)\.s[ac]ss/)
end

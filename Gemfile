source "https://rubygems.org"

# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# This will help ensure the proper Jekyll version is running.
# Happy Jekylling!
gem "jekyll", "~> 4.3"

# This is the default theme for new Jekyll sites. You may change this to anything you like.
gem "minima", "~> 2.5"

# Using GitHub Actions for deployment instead of default GitHub Pages build
# This allows us to use any Jekyll plugins without whitelist restrictions
# gem "github-pages", group: :jekyll_plugins

# Additional dependencies for Jekyll 4
gem "webrick", "~> 1.8"

# If you have any plugins, put them here!
group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-redirect-from"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
  gem "jekyll-avatar"
  gem "jemoji"
  gem "jekyll-mentions"
  # gem "jekyll-ai-domain-data"  # Temporarily disabled - requires Ruby >= 2.7.0
  gem "html-proofer"
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', platforms: [:mingw, :mswin, :x64_mingw, :jruby]


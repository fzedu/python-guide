source "https://rubygems.org"

gem "jekyll", "~> 3.9.0"

# theme
gem "jekyll-theme-midnight"

# plugins
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.6"
end

# windows does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
install_if -> { RUBY_PLATFORM =~ %r!mingw|mswin|java! } do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
end

# performance-booster for watching directories on windows
gem "wdm", "~> 0.1.0", :install_if => Gem.win_platform?

gem "kramdown-parser-gfm"
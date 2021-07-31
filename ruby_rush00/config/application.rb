require_relative "boot"
require "rails/all"

#추가 설정이 없다면 그리드의 크기는 10 * 10
$view = {"size" => [10, 10], "pos" => [0, 0]}

$game = {"Title":"", "score":"", "img":"", "font":""}

#플레이어
$player = {"hp":0, "pos":[0, 0]}


# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(*Rails.groups)

class Moviemon
  class Application < Rails::Application
    # Initialize configuration defaults for originally generated Rails version.
    config.load_defaults 6.1

    # Configuration for the application, engines, and railties goes here.
    #
    # These settings can be overridden in specific environments using the files
    # in config/environments, which are processed later.
    #
    # config.time_zone = "Central Time (US & Canada)"
    # config.eager_load_paths << Rails.root.join("extras")
  end
end

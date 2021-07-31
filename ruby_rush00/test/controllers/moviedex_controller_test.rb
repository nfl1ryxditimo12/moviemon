require "test_helper"

class MoviedexControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get moviedex_index_url
    assert_response :success
  end
end

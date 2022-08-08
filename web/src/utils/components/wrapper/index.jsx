import * as React from "react";
import { useState } from "react";
import { useHistory, useLocation, NavLink } from "react-router-dom";
import { Layout, Menu, Row, Col, Popconfirm } from "antd";
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  UserOutlined,
  TeamOutlined,
  LogoutOutlined,
  CheckOutlined,
  CalendarOutlined,
  AccountBookOutlined,
} from "@ant-design/icons";
import Utils from "utils/Utils";
import "./styles.css";

const { Header, Sider, Content } = Layout;
const { SubMenu } = Menu;
const text = "Are you sure to log out?";
/**
 * Wrapper.
 *
 * @param {Object} props
 * @param {ReactElement} props.children
 */
export default function Wrapper({ children }) {
  const history = useHistory();
  const location = useLocation();

  const [collapsed, setCollapsed] = useState(false);
  const toggle = () => {
    setCollapsed(!collapsed);
  };

  const visibleMenus = Utils.getVisibleMenus();

  const logout = Utils.logout(history);

  /**
   * processSelectedKey.
   *
   * @param {string} pathname
   * @returns {string}
   */
  const processSelectedKey = (pathname) => {
    if (pathname.startsWith("/staff")) return "/staff";
    return pathname;
  };

  return (
    <Layout className="wrapper-container" style={{ height: "120vh" }}>
      <Sider
        trigger={null}
        breakpoint="lg"
        collapsedWidth="80"
        collapsible
        collapsed={collapsed}
        onBreakpoint={(broken) => {
          setCollapsed(broken);
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            color: "white",
            width: "100%",
            height: "10vh",
            fontSize: "30px",
          }}
        >
          APTM
        </div>
        {/* <Divider /> */}
        <Menu
          className="sidebar-nav"
          selectedKeys={[processSelectedKey(location.pathname)]}
          theme="dark"
          mode="inline"
          defaultOpenKeys={["company", "", "ccf", "campaign", "survey"]}
        >
          <Menu.Item key="/" style={{ margin: "30px auto" }}>
            <NavLink exact to="/">
              <UserOutlined />
              <MenuLabel collapsed={collapsed} label="Profile" />
            </NavLink>
          </Menu.Item>
          {visibleMenus.includes("view_member") && (
            <Menu.Item key="/member" style={{ margin: "30px auto" }}>
              <NavLink to="/member">
                <TeamOutlined />
                <MenuLabel collapsed={collapsed} label="Member" />
              </NavLink>
            </Menu.Item>
          )}
          {visibleMenus.includes("view_checkin") && (
            <Menu.Item key="/check-in" style={{ margin: "30px auto" }}>
              <NavLink to="/check-in">
                <CheckOutlined />
                <MenuLabel collapsed={collapsed} label="Check In" />
              </NavLink>
            </Menu.Item>
          )}
          {visibleMenus.includes("add_service") && (
            <Menu.Item key="/manage-service" style={{ margin: "30px auto" }}>
              <NavLink to="/manage-service">
                <CalendarOutlined />
                <MenuLabel collapsed={collapsed} label="Manage Service" />
              </NavLink>
            </Menu.Item>
          )}
          {visibleMenus.includes("view_bookingservice") && (
            <SubMenu
              key="service"
              icon={<AccountBookOutlined />}
              title="Manage Subservice"
            >
              <Menu.Item key="/stay" style={{ margin: "30px auto" }}>
                <NavLink to="/manage-subservice">
                  <AccountBookOutlined />
                  <MenuLabel collapsed={collapsed} label="Subservice" />
                </NavLink>
              </Menu.Item>
              <Menu.Item key="/stay" style={{ margin: "30px auto" }}>
                <NavLink to="/manage-subservice-type">
                  <AccountBookOutlined />
                  <MenuLabel collapsed={collapsed} label="Subservice Type" />
                </NavLink>
              </Menu.Item>
              <Menu.Item key="/stay" style={{ margin: "30px auto" }}>
                <NavLink to="/manage-subservice-category">
                  <AccountBookOutlined />
                  <MenuLabel
                    collapsed={collapsed}
                    label="Subservice Category"
                  />
                </NavLink>
              </Menu.Item>
            </SubMenu>
          )}
          {visibleMenus.includes("view_event") && (
            <Menu.Item key="/event" style={{ margin: "30px auto" }}>
              <NavLink to="/event">
                <CalendarOutlined />
                <MenuLabel collapsed={collapsed} label="Event" />
              </NavLink>
            </Menu.Item>
          )}
          {visibleMenus.includes("view_eventmember") && (
            <Menu.Item key="/booking-event" style={{ margin: "30px auto" }}>
              <NavLink to="/booking-event">
                <CalendarOutlined />
                <MenuLabel collapsed={collapsed} label="Booking Event" />
              </NavLink>
            </Menu.Item>
          )}
          {visibleMenus.includes("view_bookingservice") && (
            <SubMenu
              key="service"
              icon={<AccountBookOutlined />}
              title="Booking Service"
            >
              <Menu.Item key="/stay" style={{ margin: "30px auto" }}>
                <NavLink to="/booking-stay">
                  <AccountBookOutlined />
                  <MenuLabel collapsed={collapsed} label="Booking Stay" />
                </NavLink>
              </Menu.Item>
              <Menu.Item key="/celebrate" style={{ margin: "30px auto" }}>
                <NavLink to="/booking-celebrate">
                  <AccountBookOutlined />
                  <MenuLabel collapsed={collapsed} label="Booking Celebrate" />
                </NavLink>
              </Menu.Item>
              <Menu.Item key="/dine" style={{ margin: "30px auto" }}>
                <NavLink to="/booking-dine">
                  <AccountBookOutlined />
                  <MenuLabel collapsed={collapsed} label="Booking Dine" />
                </NavLink>
              </Menu.Item>
              <Menu.Item key="/relax" style={{ margin: "30px auto" }}>
                <NavLink to="/booking-relax">
                  <AccountBookOutlined />
                  <MenuLabel collapsed={collapsed} label="Booking Relax" />
                </NavLink>
              </Menu.Item>
            </SubMenu>
          )}
        </Menu>
      </Sider>
      <Layout className="site-layout">
        <Header className="site-layout-header" style={{ padding: 0 }}>
          <Row>
            <Col span={12}>
              {React.createElement(
                collapsed ? MenuUnfoldOutlined : MenuFoldOutlined,
                {
                  className: "trigger",
                  onClick: toggle,
                }
              )}
            </Col>
            <Col span={12} className="right" style={{ paddingRight: 20 }}>
              <Popconfirm
                placement="left"
                title={text}
                onConfirm={logout}
                okText="Yes"
                cancelText="No"
              >
                <span className="pointer">
                  <span>{Utils.getStorageObj("auth").fullname}</span>
                  &nbsp;&nbsp;
                  <LogoutOutlined />
                </span>
              </Popconfirm>
            </Col>
          </Row>
        </Header>
        <Content
          className="site-layout-content"
          style={{ padding: "20px 20px" }}
        >
          {children}
        </Content>
      </Layout>
    </Layout>
  );
}

/**
 * MenuLabel.
 *
 * @param {Object} props
 * @param {boolean} props.collapsed
 * @param {string} props.label
 * @returns {ReactElement}
 */
function MenuLabel({ collapsed, label }) {
  if (collapsed) return null;
  return <span>&nbsp;{label}</span>;
}

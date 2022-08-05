import { RecoilRoot } from "recoil";
import { Switch, Route, HashRouter } from "react-router-dom";
import PrivateRoute from "utils/components/route/PrivateRoute";
import NotMatch from "utils/components/route/NotMatch";
import Utils from "utils/Utils";
import Spinner from "utils/components/spinner";
import Login from "components/account/auth/login";
import Member from "components/account/member";
import Profile from "components/account/auth/profile";
import CheckIn from "components/check_in/check";
import BookingEvent from "components/event/booking";
import ManageService from "components/service/managing/service";
import ManageSubservice from "components/service/managing/subservice";
import Event from "components/event/create";
import BookingStay from "components/service/booking/stay";
import BookingCelebrate from "components/service/booking/celebrate";
import BookingDine from "components/service/booking/dine";
import BookingRelax from "components/service/booking/relax";

Utils.responseIntercept();

function App() {
  return (
    <div>
      <RecoilRoot>
        <Spinner />
        <HashRouter>
          <Switch>
            <PrivateRoute path="/" component={Profile} exact />
            <Route path="/login" component={Login} exact />

            <PrivateRoute path="/member" component={Member} exact />

            <PrivateRoute path="/check-in" component={CheckIn} exact />

            <PrivateRoute
              path="/manage-service"
              component={ManageService}
              exact
            />
            <PrivateRoute
              path="/manage-subservice"
              component={ManageSubservice}
              exact
            />
            <PrivateRoute
              path="/manage-subservice-type"
              component={ManageSubservice}
              exact
            />
            <PrivateRoute
              path="/manage-subservice-category"
              component={ManageSubservice}
              exact
            />
            <PrivateRoute path="/event" component={Event} exact />
            <PrivateRoute
              path="/booking-event"
              component={BookingEvent}
              exact
            />

            <PrivateRoute path="/booking-stay" component={BookingStay} exact />
            <PrivateRoute
              path="/booking-celebrate"
              component={BookingCelebrate}
              exact
            />
            <PrivateRoute path="/booking-dine" component={BookingDine} exact />
            <PrivateRoute
              path="/booking-relax"
              component={BookingRelax}
              exact
            />

            <Route component={NotMatch} />
          </Switch>
        </HashRouter>
      </RecoilRoot>
    </div>
  );
}

export default App;

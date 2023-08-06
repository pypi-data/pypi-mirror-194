import jpype
import datetime

from autoai_ts_libs.deps.tspy.data_structures import TRS


@jpype.JImplements("com.ibm.research.time_series.core.utils.python.PythonObservationCollectionSupplier")
class PythonObservationCollectionSupplierImpl(object):

    @jpype.JOverride
    def get(self, tt_buffer, value_buffer, j_util, min_iat, max_iat, j_trs):
        from autoai_ts_libs.deps.tspy.data_structures.cross_language.PythonObservationCollection import PythonObservationCollection
        if j_trs is None:
            trs = None
        else:
            from autoai_ts_libs.deps.tspy.data_structures.context import get_or_create
            tsc = get_or_create()
            granularity = datetime.timedelta(
              milliseconds=j_trs.getGranularity().toMillis()
            )
            start_time = datetime.datetime.strptime(
              str(
                j_trs.getStartTime().format(
                  tsc.packages.java.time.format.DateTimeFormatter.ofPattern(
                    "yyyy-MM-dd'T'HH:mm:ss.SSSSSS[XXX]"
                  )
                )
              ),
              "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            trs = TRS(tsc, granularity, start_time, j_trs=j_trs)
        return PythonObservationCollection((tt_buffer, value_buffer, j_util), iat=(min_iat, max_iat), trs=trs)
